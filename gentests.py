#!/usr/bin/python3
import configparser
import time

from pysmapi.tester import *
import pysmapi as smapi

#smapi.set_debug(True)

config = configparser.ConfigParser(inline_comment_prefixes=("#", ";"))
config._interpolation = configparser.ExtendedInterpolation()
config.read('gentests.cfg')

THIS = config["ssi_this"]
THAT = config["ssi_that"]

PFX = THIS["pfx"]
PASS = THIS["smapipass"]
ADMIN = THIS["user"]
PING = THIS["ping"]
PONG = THIS["pong"]

VSW1 = f"{PFX}vsw1"
VSW2 = f"{PFX}vsw2"
VSWI = f"{PFX}vswi"

DISKADDR = THIS["diskaddr"]
DISKLABEL = THIS["disklabel"]

hostthis = smapi.HostInfo(host=THIS["host"],
                          port=int(THIS["port"]),
                          userid=THIS["user"],
                          password=THIS["pass"],
                          timeout=int(THIS["timeout"]),
                          ssl=THIS["ssl"] == True,
                          insecure=THIS["insecure"] == True,
                          cert=THIS["cert"])

hostthat = smapi.HostInfo(host=THAT["host"],
                          port=int(THAT["port"]),
                          userid=THAT["user"],
                          password=THAT["pass"],
                          timeout=int(THAT["timeout"]),
                          ssl=THAT["ssl"] == True,
                          insecure=THAT["insecure"] == True,
                          cert=THAT["cert"])

# =============================================================================
# Environment checks
# =============================================================================
#
# Warn user
#
print("""
WARNING: During testing the following destructive actions will be taken:

  1) The contents of the provided disk, {DISKADDR}, will be destroyed.
  2) Two randomly selected abend dumps will be processed and deleted.
  3) One randomly selected reader file from MAINT's reader will be deleted.
  4) The {system_config_fn} {system_config_ft} will be updated and is expected
     to reside on PMAINT's CF0 with default passwords.
  5) The TCPIP config will be updated and cleaned.
  6) The VSMWORK1 NAMELIST will be updated and cleaned.
  7) The directory managers volume extent config will be updated and cleaned.
  8) VSMGUARD's console spool file will be transfered to {ADMIN}'s reader
     and deleted.
""")
"""
yn = input("Continue (y/n)? ").lower().strip()
if yn != "y":
    print("Quiting...")
    quit()
"""
print()
print("Checking environment for various prereqs...")
print()

#
# Set connection info using "this" host
#
set_hostinfo(hostthis)

#
# Make sure we are authorizaed
#
gentest("Check_Authentication", None)
"""
#
# We need 2 abends dumps available for testing
#
req = gentest("Query_ABEND_Dump", None,
              target="maint",
              location="all")
dumps = []
for dump in req.abend_dump_array:
    if dump.abend_dump_loc == req.READER:
        dumps.append(dump.abend_dump_id)

if len(dumps) < 2:
    print(f"You need to have at least 2 unprocessed dumps available on")
    print(f"the '{THIS['host']}' host. Use the CP SNAPDUMP command to produce them.")
    quit()
#
# We need to have at least 1 EQID defined, but more are better
#
req = gentest("System_EQID_Query", None,
              target="maint",
              eqid_for="ALL",
              eqid_target="")
if len(req.eqid_array) == 0:
    print("Need to define some EQIDs on '{THIS['host']}'.")
    quit()

#
# Maint needs to have at least 1 file in it's reader
#
req = gentest("System_RDR_File_Query", None,
              target="maint")
if len(req.reader_file_info) == 0:
    print("Maint needs something in its reader on '{THIS['host']}'.")
    quit()

#
# Make sure the work disk is available for attaching to users
#
req = gentest("Image_Device_Dedicate", None, expect=[(-1, -1)],
              target="maint",
              image_device_number="9874",
              real_device_number=DISKADDR,
              readonly=smapi.Image_Device_Dedicate.TRUE)
if req.return_code != 0:
    print(f"The disk volume {DISKADDR} is not available for exclusive use on '{THIS['host']}'.")
    quit()

gentest("Image_Device_Undedicate", None,
        target="maint",
        image_device_number="9874")

# =============================================================================
# Image
# =============================================================================
ping=[
    "CONSOLE=VDEV=0009 DEVTYPE=3215 CLASS=T",
    "CPU=CPUADDR=00 BASE=YES",
    "CPU_MAXIMUM=COUNT=1 TYPE=ESA",
    "IPL=VDEV=CMS",
    "LINK=USERID=MAINT VDEV1=190 VDEV2=0190 MODE=RR",
    "LINK=USERID=MAINT VDEV1=19E VDEV2=019E MODE=RR",
    "MDISK=VDEV=777 DEVTYPE=XXXX DISKTYPE=AUTOG COUNT=1000 NAME=LINUX READPASSWORD=READ WRITEPASSWORD=WRITE MULTIPASSWORD=MULTIPLE",
   f"PASSWORD={PASS}",
    "PRIVILEGE_CLASSES=ABCDEFG",
    "SPOOL=VDEV=000C DEVTYPE=2540_READER CLASS=*",
    "SPOOL=VDEV=000D DEVTYPE=2540_PUNCH CLASS=A",
    "SPOOL=VDEV=000E DEVTYPE=1403 CLASS=A",
    "STORAGE_INITIAL=1G",
    "STORAGE_MAXIMUM=2G",
]

pong=[
   f"USER {PONG} {PASS} 1G 1G ABCDEFG    ",
    "  IPL CMS                           ",
    "  CONSOLE   0009 3215               ",
    "  SPOOL 00C 2540 READER *           ",
    "  SPOOL 00D 2540 PUNCH A            ",
    "  SPOOL 00E 1403 A                  ",
    "  LINK MAINT 190 190 RR             ",
    "  LINK MAINT 19E 19E RR             ",
]

gentest("Image_Definition_Async_Updates", "1",
        target=ADMIN,
        enabled="no")

gentest("Image_Deactivate", None, expect=[(-1, -1)],
        target=PING,
        force_time="immed")

gentest("Image_Delete_DM", None, expect=[(-1, -1)],
        target=PING,
        data_security_erase=smapi.Image_Delete_DM.NOERASE)

gentest("Image_Definition_Create_DM", "1", expect=[(8, 3002)],
        target=PING,
        definition_create_directory_keyword_parameter_list=["BOGUS_KEYWORD=BAD"])

gentest("Image_Definition_Create_DM", "2",
        target=PING,
        definition_create_directory_keyword_parameter_list=ping)

gentest("Image_Definition_Update_DM", "1", expect=[(8, 3002)],
        target=PING,
        definition_update_directory_keyword_parameter_list=["BOGUS_KEYWORD=BAD"])

gentest("Image_Definition_Update_DM", "2",
        target=PING,
        definition_update_directory_keyword_parameter_list=["IPL=VDEV=CMS"])

mdisk = "MDISK=OPERATION=ADD VDEV=999 COUNT=1000 DEVTYPE=XXXX DISKTYPE=AUTOG NAME=LINUX"
gentest("Image_Definition_Update_DM", "3",
        target=PING,
        definition_update_directory_keyword_parameter_list=[mdisk])

gentest("Image_Definition_Delete_DM", "1", expect=[(8, 3002)],
        target=PING,
        definition_delete_directory_keyword_parameter_list=["BOGUS_KEYWORD=BAD"])

gentest("Image_Definition_Delete_DM", "2",
        target=PING,
        definition_delete_directory_keyword_parameter_list=["MDISK=VDEV=999"])

gentest("Image_Definition_Query_DM", "1", expect=[(8, 3002)],
        target=PING,
        definition_query_directory_keyword_parameter_list=["BOGUS_KEYWORD=BAD"])

gentest("Image_Definition_Query_DM", "2",
        target=PING,
        definition_query_directory_keyword_parameter_list=["MDISK"])

gentest("Image_Definition_Query_DM", "3",
        target=PING,
        definition_query_directory_keyword_parameter_list=["*"])

gentest("Image_Activate", "1",
        target=PING)

# ==========

gentest("Image_Deactivate", None, expect=[(-1, -1)],
        target=PONG,
        force_time="immed")

gentest("Image_Delete_DM", None, expect=[(-1, -1)],
        target=PONG,
        data_security_erase=smapi.Image_Delete_DM.NOERASE)

gentest("Image_Create_DM", "1",
        target=PONG,
        image_record_array=pong)

gentest("Image_Lock_DM", "1",
        target=PONG,
        device_address="888")

gentest("Image_Lock_Query_DM", "1", expect=[(0,12)],
        target=PONG)

gentest("Image_Unlock_DM", "1",
        target=PONG,
        device_address="888")

gentest("Image_Lock_DM", None,
        target=PONG)

gentest("Image_Replace_DM", "1",
        target=PONG,
        image_record_array=pong)

gentest("Image_Password_Set_DM", "1",
        target=PONG,
        image_password=f"{PASS}")

gentest("Image_CPU_Set_Maximum_DM", "1",
        target=PONG,
        max_cpu=4)

gentest("Image_CPU_Define_DM", "1",
        target=PONG,
        cpu_address="00",
        base_cpu=smapi.Image_CPU_Define_DM.BASE,
        cpuid="123456",
        dedicate_cpu=smapi.Image_CPU_Define_DM.NODEDICATE,
        crypto=smapi.Image_CPU_Define_DM.UNSPECIFIED)

gentest("Image_CPU_Query_DM", "1",
        target=PONG,
        cpu_address="00")

gentest("Image_CPU_Delete_DM", "1",
        target=PONG,
        cpu_address="00")

gentest("Image_Disk_Create_DM", None,
        target=PONG,
        image_disk_number="888",
        image_disk_device_type="3390",
        image_disk_allocation_type="AUTOG",
        allocation_area_name_or_volser="LINUX",
        allocation_unit_size=smapi.Image_Disk_Create_DM.CYLINDERS,
        image_disk_size=10,
        image_disk_mode="W",
        image_disk_formatting=smapi.Image_Disk_Create_DM.BLK4096,
        image_disk_label="DSK888",
        read_password="READ",
        write_password="WRITE",
        multi_password="MULTIPLE")

gentest("Image_SCSI_Characteristics_Define_DM", "1",
        target=PONG,
        boot_program="1",
        br_lba="0123456789ABCDEF",
        lun="5241000000000000",
        port_name="5005076300c20b8e",
        scp_data_type=smapi.Image_SCSI_Characteristics_Define_DM.HEX,
        scp_data=b"\xf0\xf1\xf2\xf3")

gentest("Image_SCSI_Characteristics_Query_DM", "1",
        target=PONG)

# We're going to set a bogus IPL address so that PONG will not
# be using an NSS which might prevent LGR below.
gentest("Image_IPL_Delete_DM", "1",
        target=PONG)

gentest("Image_IPL_Set_DM", "1",
        target=PONG,
        saved_system="888",
        load_parameter="LOAD",
        parameter_string="PARM")

gentest("Image_IPL_Query_DM", "1",
        target=PONG)

gentest("Image_Activate", None,
        target=PONG)

gentest("Image_Query_Activate_Time", "1",
        target=PONG,
        date_format_indicator=smapi.Image_Query_Activate_Time.MMDDYYYY)

gentest("VMRELOCATE_Image_Attributes", "1",
        target=PONG,
        relocation_setting="ON",
        domain_name="SSI",
        archforce="NO")

# Result is due to HCP1926E but this is fine since input and output
# processing is still tested.
gentest("VMRELOCATE_Modify", "1", expect=[(8, 3010)],
        target=PONG,
        max_total="500",
        max_quiesce="400")

# This attempt will fail because the guest has two LINKs defined, causing
# HCP1996I and HCP1981I.  This is good since error processing is tested.
gentest("VMRELOCATE", "1", expect=[(4, 3000)],
        target=PONG,
        destination=THAT["node"],
        action="test",
        force="domain storage")

# Now detach the two LINKs and the next VMRELOCATE should succeed
gentest("Image_Disk_Unshare", "1",
        target=PONG,
        image_disk_number="190")
gentest("Image_Disk_Unshare", None,
        target=PONG,
        image_disk_number="19E")

# Migrate PONG from THIS to THAT node
gentest("VMRELOCATE", "2",
        target=PONG,
        destination=THAT["node"],
        action="move",
        force="domain storage",
        immediate="no",
        max_total="nolimit",
        max_quiesce="nolimit")

# Possibly no active relocations
gentest("VMRELOCATE_Status", "1", expect=[(0,0), (4, 3001)],
        target=PONG,
        status_target="ALL")

# Switch to THAT host to migrate PONG back to THIS host.
set_hostinfo(hostthat)

# Migrate PONG from THAT node to THIS node
gentest("VMRELOCATE", "3",
        target=PONG,
        destination=THIS["node"],
        action="move",
        force="domain storage",
        immediate="yes")

# Possibly no active relocations
gentest("VMRELOCATE_Status", "1", expect=[(0,0), (4, 3001)],
        target=PONG,
        status_target="ALL")

# Reset to THIS host
set_hostinfo(hostthis)

# Must replace IPL statement with valid one and recycle user so the
# system doesn't automatically force the user due to inactivity.
gentest("Image_IPL_Delete_DM", None,
        target=PONG)
gentest("Image_IPL_Set_DM", None,
        target=PONG,
        saved_system="CMS",
        load_parameter="",
        parameter_string="")

# Finally recycle the user to get CMS going
gentest("Image_Recycle", "1",
        target=PONG)

gentest("Image_Disk_Create_DM", "1",
        target=PONG,
        image_disk_number="999",
        image_disk_device_type="3390",
        image_disk_allocation_type="AUTOG",
        allocation_area_name_or_volser="LINUX",
        allocation_unit_size=smapi.Image_Disk_Create_DM.CYLINDERS,
        image_disk_size=10,
        image_disk_mode="W",
        image_disk_formatting=smapi.Image_Disk_Create_DM.BLK4096,
        image_disk_label="DSK999",
        read_password="READ",
        write_password="WRITE",
        multi_password="MULTIPLE")

gentest("Image_Disk_Create", "1",
        target=PONG,
        image_disk_number="999",
        image_disk_mode="MR") 

gentest("Image_Disk_Copy_DM", "1",
        target=PONG,
        image_disk_number="777",
        source_image_name=PING,
        source_image_disk_number="777",
        image_disk_allocation_type="AUTOG",
        allocation_area_name_or_volser="LINUX",
        image_disk_mode="W",
        read_password="READ",
        write_password="WRITE",
        multi_password="MULTIPLE")

gentest("Image_Disk_Copy", "1",
        target=PONG,
        image_disk_number="777")

gentest("Image_Disk_Query", "1",
        target="maint",
        vdasd_id="ALL")

gentest("Image_Disk_Share_DM", "1",
        target=PONG,
        target_image_name=PING,
        image_disk_number="777",
        target_image_disk_number="555",
        read_write_mode="MR",
        optional_password="MULTIPLE")

gentest("Image_Disk_Unshare_DM", "1",
        target=PONG,
        target_image_name=PING,
        image_disk_number="777",
        target_image_disk_number="555")

gentest("Image_Disk_Share", "1",
        target=PONG,
        target_image_name=PING,
        image_disk_number="557",
        target_image_disk_number="777",
        read_write_mode="MW",
        optional_password="MULTIPLE")

gentest("Image_Disk_Unshare", "1",
        target=PONG,
        image_disk_number="557")

gentest("Image_Disk_Delete", "1",
        target=PONG,
        image_disk_number="999")

gentest("Image_Disk_Delete_DM", "1",
        target=PONG,
        image_disk_number="999",
        data_security_erase=smapi.Image_Disk_Delete_DM.NOERASE)

gentest("Image_Device_Dedicate_DM", "1",
        target=PONG,
        image_device_number="3000",
        real_device_number=DISKADDR,
        readonly=smapi.Image_Device_Dedicate.TRUE)

gentest("Image_Device_Dedicate", "1",
        target=PONG,
        image_device_number="3000",
        real_device_number=DISKADDR,
        readonly=smapi.Image_Device_Dedicate.TRUE)

gentest("Image_Device_Reset", "1",
        target=PONG,
        image_device_number="3000")

gentest("Image_Device_Undedicate_DM", "1",
        target=PONG,
        image_device_number="3000")

gentest("Image_Device_Undedicate", "1",
        target=PONG,
        image_device_number="3000")

gentest("Image_Active_Configuration_Query", "1",
        target=PONG)

gentest("Image_Pause", "1",
        target=PONG,
        action="pause")

gentest("Image_Pause", None,
        target=PONG,
        action="unpause")

gentest("Image_Status_Query", "1",
        target=PONG)

gentest("Image_CPU_Define", "1",
        target=PONG,
        cpu_address="01",
        cpu_type=smapi.Image_CPU_Define.IFL)

gentest("Image_CPU_Query", "1",
        target=PONG)

gentest("Image_CPU_Delete", "1",
        target=PONG,
        cpu_address="01")

gentest("Image_Query_DM", "1",
        target=PONG)

gentest("Image_Name_Query_DM", "1",
        target=ADMIN)

gentest("Image_Console_Get", "1",
        target="vsmguard")

gentest("Image_MDISK_Link_Query", "1",
        target="tcpip",
        vdev="592")

gentest("Image_Volume_Share", "1",
        target=ADMIN,
        img_vol_addr=DISKADDR,
        share_enable="ON")

gentest("Image_Volume_Add", "1",
        target=ADMIN,
        image_device_number=DISKADDR,
        image_vol_id=DISKLABEL,
        system_config_name=THIS["syscfg_fn"],
        system_config_type=THIS["syscfg_ft"],
        parm_disk_owner=THIS["syscfg_owner"],
        parm_disk_number=THIS["syscfg_mdisk"],
        parm_disk_password=THIS["syscfg_multi"],
        alt_system_config_name=THIS["altcfg_fn"],
        alt_system_config_type=THIS["altcfg_ft"],
        alt_parm_disk_owner=THIS["altcfg_owner"],
        alt_parm_disk_number=THIS["altcfg_mdisk"],
        alt_parm_disk_password=THIS["altcfg_multi"])

gentest("Image_Volume_Delete", "1",
        target="maint",
        image_device_number=DISKADDR,
        image_vol_id=DISKLABEL,
        system_config_name=THIS["syscfg_fn"],
        system_config_type=THIS["syscfg_ft"],
        parm_disk_owner=THIS["syscfg_owner"],
        parm_disk_number=THIS["syscfg_mdisk"],
        parm_disk_password=THIS["syscfg_multi"],
        alt_system_config_name=THIS["altcfg_fn"],
        alt_system_config_type=THIS["altcfg_ft"],
        alt_parm_disk_owner=THIS["altcfg_owner"],
        alt_parm_disk_number=THIS["altcfg_mdisk"],
        alt_parm_disk_password=THIS["altcfg_multi"])

# =============================================================================
# Image
# =============================================================================

gentest("Image_Volume_Space_Define_DM", "1",
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Define_DM.FT_1,
        image_vol_id="TST001",
        region_name="RGN001",
        start_cylinder=1,
        size=32760,
        device_type=smapi.Image_Volume_Space_Define_DM.DT_3390)

gentest("Image_Volume_Space_Define_DM", "2",
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Define_DM.FT_5,
        region_name="RGN001",
        group_name="GRP001")

gentest("Image_Volume_Space_Define_Extended_DM", "1",
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Define_Extended_DM.FT_2,
        image_vol_id="TST002",
        region_name="RGN002",
        start_cylinder=1,
        size=32760,
        group_name="GRP001",
        device_type=smapi.Image_Volume_Space_Define_Extended_DM.DT_3390)

gentest("Image_Volume_Space_Define_Extended_DM", "2",
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Define_Extended_DM.FT_1,
        image_vol_id="TST003",
        region_name="RGN003",
        start_cylinder=1,
        size=32760,
        device_type=smapi.Image_Volume_Space_Define_Extended_DM.DT_3390)

gentest("Image_Volume_Space_Define_Extended_DM", "3",
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Define_Extended_DM.FT_5,
        region_name="RGN003",
        group_name="GRP001",
        alloc_method=smapi.Image_Volume_Space_Define_Extended_DM.AM_1)

gentest("Image_Volume_Space_Query_DM", "1",
        target=ADMIN,
        query_type=smapi.Image_Volume_Space_Query_DM.USED,
        entry_type=smapi.Image_Volume_Space_Query_DM.REGION,
        entry_names="*")

gentest("Image_Volume_Space_Query_Extended_DM", "1",
        target=ADMIN,
        query_type=smapi.Image_Volume_Space_Query_Extended_DM.USED,
        entry_type=smapi.Image_Volume_Space_Query_Extended_DM.REGION,
        entry_names="*")

gentest("Image_Volume_Space_Remove_DM", "1",
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Remove_DM.FT_7,
        group_name="GRP001")

gentest("Image_Volume_Space_Remove_DM", "2",
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Remove_DM.FT_3,
        region_name="RGN001"),

gentest("Image_Volume_Space_Remove_DM", None,
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Remove_DM.FT_6,
        image_vol_id="TST001")

gentest("Image_Volume_Space_Remove_DM", None,
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Remove_DM.FT_6,
        image_vol_id="TST002")

gentest("Image_Volume_Space_Remove_DM", None,
        target=ADMIN,
        function_type=smapi.Image_Volume_Space_Remove_DM.FT_6,
        image_vol_id="TST003")

# =============================================================================
# Abend dumps
# =============================================================================
req = gentest("Query_ABEND_Dump", "1",
              target=ADMIN,
              location="all")

dumps = []
for dump in req.abend_dump_array:
    if dump.abend_dump_loc == req.READER:
        dumps.append(dump.abend_dump_id)


gentest("Process_ABEND_Dump", "1",
        target=ADMIN,
        spoolid=dumps[0])

gentest("Delete_ABEND_Dump", "1",
        target=ADMIN,
        id=dumps[1])
# =============================================================================
# Notification
# =============================================================================

gentest("Asynchronous_Notification_Enable_DM", "1",
        target=ADMIN,
        entity_type=smapi.Asynchronous_Notification_Enable_DM.DIRECTORY,
        subscription_type=smapi.Asynchronous_Notification_Enable_DM.INCLUDE,
        communication_type=smapi.Asynchronous_Notification_Enable_DM.TCP,
        port_number=5000,
        ip_address="192.168.1.1",
        encoding=smapi.Asynchronous_Notification_Enable_DM.EBCDIC,
        subscriber_data="subdata")

gentest("Asynchronous_Notification_Query_DM", "1",
        target=ADMIN,
        entity_type=smapi.Asynchronous_Notification_Query_DM.DIRECTORY,
        communication_type=smapi.Asynchronous_Notification_Query_DM.TCP,
        port_number=5000,
        ip_address="192.168.1.1",
        encoding=smapi.Asynchronous_Notification_Query_DM.EBCDIC,
        subscriber_data="subdata")

gentest("Asynchronous_Notification_Disable_DM", "1",
        target=ADMIN,
        entity_type=smapi.Asynchronous_Notification_Disable_DM.DIRECTORY,
        communication_type=smapi.Asynchronous_Notification_Disable_DM.TCP,
        port_number=5000,
        ip_address="192.168.1.1",
        encoding=smapi.Asynchronous_Notification_Disable_DM.EBCDIC,
        subscriber_data="subdata")

gentest("Authorization_List_Add", "1",
        target=PING,
        for_id="all",
        function_id="all")

gentest("Authorization_List_Query", "1",
        target="",
        for_id="*",
        function_id="*")

gentest("Authorization_List_Remove", "1",
        target=PING,
        for_id="all",
        function_id="all")

gentest("Directory_Manager_Local_Tag_Define_DM", "1",
        target=ADMIN,
        tag_name="Tag1",
        tag_ordinal=1,
        define_action=smapi.Directory_Manager_Local_Tag_Define_DM.CREATE)

gentest("Directory_Manager_Local_Tag_Set_DM", "1",
        target=PING,
        tag_name="Tag1",
        tag_value="Val1")

gentest("Directory_Manager_Local_Tag_Query_DM", "1",
        target=PING,
        tag_name="Tag1")

gentest("Directory_Manager_Local_Tag_Set_DM", None,
        target=PING,
        tag_name="Tag1",
        tag_value="DELETE")

gentest("Directory_Manager_Local_Tag_Delete_DM", "1",
        target=ADMIN,
        tag_name="Tag1")

gentest("Directory_Manager_Search_DM", "1",
        target=ADMIN,
        search_pattern="user sys*")

# This will fail, but at least it checks the key handling
gentest("Directory_Manager_Task_Cancel_DM", "1", expect=[(452,4)],
        target=ADMIN,
        operation_id=1234)

gentest("Event_Subscribe", "1",
        target=ADMIN,
        match_key="")

gentest("Event_Unsubscribe", "1",
        target=ADMIN)

# =============================================================================
# Image
# =============================================================================

gentest("Metadata_Set", "1",
        target=ADMIN,
        metadata_entry_array=[["key1", "val1"], ["key2", "val2"]])

gentest("Metadata_Get", "1",
        target=ADMIN,
        metadata_name_list="md_name1 md_name2")

gentest("Metadata_Space_Query", "1",
        target=ADMIN,
        searchkey="*")

gentest("Name_List_Add", "1", expect=[(0,12)],
        target="userlist",
        name="myname")

gentest("Name_List_Add", "1",
        target="userlist",
        name="yourname")

gentest("Name_List_Query", "1",
        target="*")

gentest("Name_List_Remove", "1",
        target="userlist",
        name="myname")

gentest("Name_List_Destroy", "1",
        target="userlist")

# We want the page volume add to fail so we don't have to manually remove
# it later.  This is done by attaching the device to PONG.
gentest("Image_Device_Dedicate", None,
        target=PONG,
        image_device_number="3000",
        real_device_number=DISKADDR,
        readonly=smapi.Image_Device_Dedicate.TRUE)

# This will fail, but it still exercises the API input and output.
gentest("Page_or_Spool_Volume_Add", "1", expect=[(8, 3003)],
        target=ADMIN,
        vol_addr=DISKADDR,
        volume_label=DISKLABEL,
        volume_use="PAGE",
        system_config_name=THIS["syscfg_fn"],
        system_config_type=THIS["syscfg_ft"],
        parm_disk_owner=THIS["syscfg_owner"],
        parm_disk_number=THIS["syscfg_mdisk"],
        parm_disk_password=THIS["syscfg_multi"])

gentest("Image_Device_Undedicate", None,
        target=PONG,
        image_device_number="3000")

gentest("Query_All_DM", "1",
        target=ADMIN,
        query_keyword_parameter_list="format=no")

gentest("Query_All_DM", "2",
        target=ADMIN,
        query_keyword_parameter_list="format=yes")

# Expected to fail
gentest("Query_Asynchronous_Operation_DM", "1",
        target=ADMIN,
        operation_id=1234)

gentest("Shared_Memory_Create", "1",
        target=PING,
        memory_segment_name="SHAREMEM",
        begin_page=0xF000,
        end_page=0xF0FF,
        page_access_descriptor=smapi.Shared_Memory_Create.SW,
        memory_attributes=smapi.Shared_Memory_Create.RSTD,
        memory_access_identifier=ADMIN)

gentest("Shared_Memory_Replace", "1", expect=[(0, 12)],
        target=PING,
        memory_segment_name="SHAREMEM",
        memory_access_identifier=ADMIN)

gentest("Shared_Memory_Query", "1",
        target=ADMIN,
        memory_segment_name="*")

gentest("Shared_Memory_Delete", "1",
        target=PING,
        memory_segment_name="SHAREMEM")

# Shared_Memory_Delete doesn't remove access that was given with
# Shared_Memory_Create, so do it manually here.
gentest("Shared_Memory_Access_Remove_DM", None,
        target=ADMIN,
        memory_segment_name="SHAREMEM")

gentest("Shared_Memory_Access_Add_DM", "1",
        target=ADMIN,
        memory_segment_name="SHAREMEM")

gentest("Shared_Memory_Access_Query_DM", "1",
        target=ADMIN,
        memory_segment_name="SHAREMEM")

gentest("Shared_Memory_Access_Remove_DM", "1",
        target=ADMIN,
        memory_segment_name="SHAREMEM")

gentest("System_Disk_IO_Query", "1",
        target=ADMIN,
        system_disk_io_list="rdev=*")

gentest("System_Disk_Query", "1",
        target=ADMIN,
        dev_num='ALL')

req = gentest("System_EQID_Query", "1",
              target=ADMIN,
              eqid_for="ALL",
              eqid_target="")

gentest("System_EQID_Query", "2",
        target=ADMIN,
        eqid_for="RDEV",
        eqid_target=req.eqid_array[0].eqid_rdev)

gentest("System_EQID_Query", "3",
        target=ADMIN,
        eqid_for="EQID",
        eqid_target=req.eqid_array[0].eqid_name)

gentest("System_EQID_Query", "4", expect=[(8,3003)],
        target=ADMIN,
        eqid_for="RDEV",
        eqid_target=req.eqid_array[0].eqid_rdev + ",9999")

gentest("System_FCP_Free_Query", "1", expect=[(0,0), (8,8)],
        target=ADMIN,
        fcp_dev=5000)

gentest("System_Information_Query", "1",
        target=ADMIN)

gentest("System_Page_Utilization_Query", "1",
        target=ADMIN)

gentest("System_Performance_Information_Query", "1",
        target=ADMIN,
        system_performance_information_list=["DETAILED_CPU=SHOW=YES", "MONITOR_EVENT=QUERY=NO"])

gentest("System_Performance_Threshold_Enable", "1",
        target=ADMIN,
        event_type="system_cpu=99")

gentest("System_Performance_Threshold_Disable", "1",
        target=ADMIN,
        event_type="system_cpu")

req = gentest("System_RDR_File_Query", "1",
              target="maint")

gentest("System_RDR_File_Manage", "1",
        target=ADMIN,
        spoolids=req.reader_file_info[0].file,
        action="PURGE")

# This will fail since we don't have any valid FCP devices
gentest("System_SCSI_Disk_Add", "1", expect=[(0, 0), (396, 8700)],
        target="maint",
        dev_num="7000",
        dev_path_array="5000 0000000000000001 0000000000000001",
        option="1",
        persist="NO")

gentest("System_SCSI_Disk_Query", "1",
        target=PING,
        dev_num="ALL")

gentest("System_SCSI_Disk_Delete", "1",
        target=PING,
        dev_num="7000",
        persist="NO")

gentest("System_Service_Query", "1",
        target=ADMIN,
        system_service_query_list=["component=namecomponent=cp type=rsu"])

gentest("System_Spool_Utilization_Query", "1",
        target=ADMIN)

req = gentest("VMRM_Configuration_Query", "1",
              target=ADMIN,
              configuration_file_name=THIS["vmrm_fn"],
              configuration_file_type=THIS["vmrm_ft"],
              configuration_dir_name=THIS["vmrm_dir"])

gentest("VMRM_Configuration_Update", "1",
        target=ADMIN,
        configuration_file_name=THIS["vmrm_fn"],
        configuration_file_type=THIS["vmrm_ft"],
        configuration_dir_name=THIS["vmrm_dir"],
        syncheck_only=True,
        update_file=req.configuration_file)

gentest("VMRM_Measurement_Query", "1",
        target=ADMIN)

gentest("Virtual_Channel_Connection_Create", "1",
        target=PING,
        image_device_number="f100",
        coupled_image_name=PING,
        coupled_image_device_number="f200")

gentest("Virtual_Channel_Connection_Create_DM", "1",
        target=PING,
        image_device_number="f100",
        coupled_image_name=PING)

gentest("Virtual_Channel_Connection_Delete", "1",
        target=PING,
        image_device_number="f100")

gentest("Virtual_Channel_Connection_Delete_DM", "1",
        target=PING,
        image_device_number="f100")

# All settings are exercised (at least on our side)
gentest("Virtual_Network_Vswitch_Create", "1",
        target=ADMIN,
        switch_name=VSW1,
        real_device_address="NONE",
        port_name="name1 name2 name3",
        controller_name="*",
        connection_value=smapi.Virtual_Network_Vswitch_Create.NOACTIVATE,
        queue_memory_limit=8,
        #routing_value=smapi.Virtual_Network_Vswitch_Create.UNSPECIFIED,
        transport_type=smapi.Virtual_Network_Vswitch_Create.IP,
        vlan_id=smapi.Virtual_Network_Vswitch_Create.NOTSPECIFIED,
        port_type=smapi.Virtual_Network_Vswitch_Create.UNSPECIFIED,
        update_system_config_indicator=smapi.Virtual_Network_Vswitch_Create.CREATEADD,
        system_config_name=THIS["syscfg_fn"],
        system_config_type=THIS["syscfg_ft"],
        parm_disk_owner=THIS["syscfg_owner"],
        parm_disk_number=THIS["syscfg_mdisk"],
        parm_disk_password=THIS["syscfg_multi"],
        alt_system_config_name=THIS["altcfg_fn"],
        alt_system_config_type=THIS["altcfg_ft"],
        alt_parm_disk_owner=THIS["altcfg_owner"],
        alt_parm_disk_number=THIS["altcfg_mdisk"],
        alt_parm_disk_password=THIS["altcfg_multi"],
        gvrp_value=smapi.Virtual_Network_Vswitch_Create.UNSPECIFIED,
        native_vlanid=smapi.Virtual_Network_Vswitch_Create.NOTSPECIFIED)

gentest("Virtual_Network_Vswitch_Set", "1",
        target=ADMIN,
        switch_name=VSW1,
        grant_userid=PONG)

gentest("Network_IP_Interface_Create", "1",
        target=ADMIN,
        tcpip_stack="tcpip",
        interface_id="eth99",
        permanent="no",
        primary_ipv4="192.168.1.99",
        interface=f"VETH F100 SYSTEM {VSW1}",
        cpu="0",
        transport_type="IP",
        mtu="0",
        noforward="OFF",
        pathmtu="yes",
        port_name="name1",
        port_number="3",
        vlan="43")

gentest("Network_IP_Interface_Modify", "1",
        target=ADMIN,
        tcpip_stack="tcpip",
        interface_id="eth99",
        permanent="no",
        add_ip="192.168.1.99/28")

gentest("Network_IP_Interface_Query", "1",
        target=ADMIN,
        tcpip_stack="tcpip",
        interface_id="eth99")

gentest("Network_IP_Interface_Remove", "1",
        target=ADMIN,
        tcpip_stack="tcpip",
        interface_id="eth99",
        permanent="no")

# All but the vswitch_domain can be specified here
gentest("Virtual_Network_Vswitch_Create_Extended", "2",
        target=ADMIN,
        switch_name=VSW2,
        real_device_address="600 610",
        port_name="name1 name2 name3",
        controller_name="*",
        connection_value="DISCON",
        queue_memory_limit="8",
        routing_value="",
        transport_type="ETHERNET",
        vlan_id="1024",
        port_type="TRUNK",
        persist="NO",
        gvrp_value="GVRP",
        native_vlanid="2049",
        vswitch_type="QDIO",
        iptimeout="5",
        port_selection="PORTBASED",
        vswitch_global="LOCAL")

# An IVL vswitch used the vswitch_domain setting
gentest("Virtual_Network_Vswitch_Create_Extended", "3",
        target=ADMIN,
        switch_name=VSWI,
        real_device_address="620 630",
        connection_value="DISCON",
        transport_type="ETHERNET",
        vlan_id="1024",
        persist="NO",
        native_vlanid="2049",
        vswitch_type="IVL",
        vswitch_domain="B",
        vswitch_global="DOMAIN")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "1",
        target=ADMIN,
        switch_name=VSW2,
        real_device_address="NONE",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "2",
        target=ADMIN,
        switch_name=VSW2,
        port_name="pn1 pn2 pn3",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "3",
        target=ADMIN,
        switch_name=VSW2,
        controller_name="*",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "4",
        target=ADMIN,
        switch_name=VSW2,
        connection_value="DISCONNECT",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "5",
        target=ADMIN,
        switch_name=VSW2,
        queue_memory_limit="8",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "6",
        target=ADMIN,
        switch_name=VSW2,
        gvrp_value="GVRP",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "7",
        target=ADMIN,
        switch_name=VSW2,
        mac_id="123456",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "8",
        target=ADMIN,
        switch_name=VSW2,
        portnum=f"200 {PING}",
        uplink="NO",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "9",
        target=ADMIN,
        switch_name=VSW2,
        nic_userid=PONG,
        nic_vdev="FF00",
        nic_portselection="AUTO",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "10",
        target=ADMIN,
        switch_name=VSWI,
        lacp="ACTIVE",
        lacp_group_type="EXCLUSIVE",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "11",
        target=ADMIN,
        switch_name=VSW2,
        interval="1",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "12",
        target=ADMIN,
        switch_name=VSW2,
        group_rdev="640 650",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "13",
        target=ADMIN,
        switch_name=VSW2,
        iptimeout="240",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "14",
        target=ADMIN,
        switch_name=VSW2,
        port_isolation="OFF",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "15",
        target=ADMIN,
        switch_name=VSW2,
        MAC_protect="ON",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "16",
        target=ADMIN,
        switch_name=VSW2,
        VLAN_counters="ON",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "17",
        target=ADMIN,
        switch_name=VSW2,
        vepa="ON",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "18",
        target=ADMIN,
        switch_name=VSW2,
        trace_size="8",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "19",
        target=ADMIN,
        switch_name=VSWI,
        ivl_vlanid="1000",
        persist="NO")

# Set general parameters
gentest("Virtual_Network_Vswitch_Set_Extended", "20",
        target=ADMIN,
        switch_name=VSWI,
        ivl_heartbeat="30",
        persist="NO")

# Grant user
gentest("Virtual_Network_Vswitch_Set_Extended", "21",
        target=ADMIN,
        switch_name=VSW2,
        grant_userid=PING,
        user_vlan_id="1-256",
        port_type="TRUNK",
        promiscuous="YES",
        persist="NO")

# Grant user
gentest("Virtual_Network_Vswitch_Set_Extended", "22",
        target=ADMIN,
        switch_name=VSW2,
        portnum=f"100 {PING}",
        user_vlan_id="1-256",
        port_type="TRUNK",
        promiscuous="YES",
        persist="NO")

# Grant user
gentest("Virtual_Network_Vswitch_Set_Extended", "23",
        target=ADMIN,
        switch_name=VSW2,
        revoke_userid=PING,
        persist="NO")

gentest("Virtual_Network_Vswitch_Query", "1",
        target=ADMIN,
        switch_name="*")

gentest("Virtual_Network_Vswitch_Query_Byte_Stats", "1",
        target=ADMIN,
        switch_name="*")

gentest("Virtual_Network_Vswitch_Query_Extended", "1",
        target=ADMIN,
        switch_name="*",
        vepa_status="YES")

gentest("Virtual_Network_Vswitch_Query_Stats", "1",
        target=ADMIN,
        switch_name="GT@VSW1",
        fmt_version="4")

# Remove VLAN port range
gentest("Virtual_Network_Vswitch_Set_Extended", "3",
        target=ADMIN,
        switch_name=VSW2,
        persist="NO",
        vlan_port_remove="200 128-256")

# Delete VLAN
gentest("Virtual_Network_Vswitch_Set_Extended", "4",
        target=ADMIN,
        switch_name=VSW2,
        persist="NO",
        vlan_delete="100")

# Revoke user
gentest("Virtual_Network_Vswitch_Set_Extended", "6",
        target=ADMIN,
        switch_name=VSW2,
        revoke_userid=PING)

gentest("Virtual_Network_Vswitch_Delete", "1",
        target=ADMIN,
        switch_name=VSW1,
        update_system_config_indicator=smapi.Virtual_Network_Vswitch_Delete.BOTH,
        system_config_name=THIS["syscfg_fn"],
        system_config_type=THIS["syscfg_ft"],
        parm_disk_owner=THIS["syscfg_owner"],
        parm_disk_number=THIS["syscfg_mdisk"],
        parm_disk_password=THIS["syscfg_multi"],
        alt_system_config_name=THIS["altcfg_fn"],
        alt_system_config_type=THIS["altcfg_ft"],
        alt_parm_disk_owner=THIS["altcfg_owner"],
        alt_parm_disk_number=THIS["altcfg_mdisk"],
        alt_parm_disk_password=THIS["altcfg_multi"])

gentest("Virtual_Network_Vswitch_Delete_Extended", "1",
        target=ADMIN,
        switch_name=VSW2,
        persist="NO")

gentest("Virtual_Network_Vswitch_Delete_Extended", None,
        target=ADMIN,
        switch_name=VSWI,
        persist="NO")
"""
gentest("Virtual_Network_LAN_Create", "1",
        target=ADMIN,
        lan_name=VSW1,
        lan_owner="SYSTEM",
        lan_type=smapi.Virtual_Network_LAN_Create.LT_4,
        transport_type=smapi.Virtual_Network_LAN_Create.IP)

gentest("Virtual_Network_LAN_Query", "1",
        target=ADMIN,
        lan_name=VSW1,
        lan_owner="SYSTEM")

gentest("Virtual_Network_LAN_Access", "1",
        target=ADMIN,
        lan_name=VSW1,
        lan_owner="SYSTEM",
        access_op="GRANT",
        access_user=PONG,
        promiscuity="NONPROMISCUOUS")

gentest("Virtual_Network_LAN_Access", None,
        target=ADMIN,
        lan_name=VSW1,
        lan_owner="SYSTEM",
        access_op="GRANT",
        access_user=PING,
        promiscuity="PROMISCUOUS")

gentest("Virtual_Network_LAN_Access_Query", "1",
        target=ADMIN,
        lan_name=VSW1,
        lan_owner="SYSTEM")

gentest("Virtual_Network_Adapter_Create", "1",
        target=PONG,
        image_device_number="9000",
        adapter_type=smapi.Virtual_Network_Adapter_Create.QDIO,
        network_adapter_devices=3,
        channel_path_type_id="")

gentest("Virtual_Network_Adapter_Create_DM", "1",
        target=PONG,
        image_device_number="9000",
        adapter_type=smapi.Virtual_Network_Adapter_Create_DM.QDIO,
        network_adapter_devices=3,
        channel_path_id="31")

gentest("Virtual_Network_Adapter_Create_Extended", "1",
        target=PONG,
        image_device_number="9100",
        adapter_type="qdio",
        devices="3")

gentest("Virtual_Network_Adapter_Create_Extended_DM", "1",
        target=PONG,
        image_device_number="9100",
        adapter_type="qdio",
        devices="3",
        channel_path_id="31")

gentest("Virtual_Network_Adapter_Connect_LAN", "1",
        target=PONG,
        image_device_number="9000",
        lan_name=VSW1,
        lan_owner="SYSTEM")

gentest("Virtual_Network_Adapter_Connect_LAN_DM", "1",
        target=PONG,
        image_device_number="9000",
        lan_name=VSW1,
        lan_owner="SYSTEM")

gentest("Virtual_Network_Adapter_Connect_Vswitch", "1",
        target=PONG,
        image_device_number="9100",
        switch_name=VSW1)

gentest("Virtual_Network_Adapter_Connect_Vswitch_DM", "1",
        target=PONG,
        image_device_number="9100",
        switch_name=VSW1)

gentest("Virtual_Network_Adapter_Create_Extended", None,
        target=PONG,
        image_device_number="9200",
        adapter_type="qdio",
        devices="3",
        channel_path_id="31")

gentest("Virtual_Network_Adapter_Connect_Vswitch_Extended", "1",
        target=PONG,
        image_device_number="9200",
        switch_name=VSW1)

gentest("Virtual_Network_Adapter_Query", "1",
        target=PONG,
        image_device_number="*")

gentest("Virtual_Network_Adapter_Query_Extended", "1",
        target=PONG,
        image_device_number="*")

gentest("Virtual_Network_Adapter_Disconnect", "1",
        target=PONG,
        image_device_number="9000")

gentest("Virtual_Network_Adapter_Disconnect_DM", "1",
        target=PONG,
        image_device_number="9000")

gentest("Virtual_Network_Adapter_Delete", "1",
        target=PONG,
        image_device_number="9000")

gentest("Virtual_Network_Adapter_Delete_DM", "1",
        target=PONG,
        image_device_number="9000")

gentest("Virtual_Network_LAN_Delete", "1",
        target=ADMIN,
        lan_name=VSW1,
        lan_owner="SYSTEM")

gentest("Virtual_Network_VLAN_Query_Stats", "1",
        target=ADMIN,
        userid="tcpip",
        device="BOTH")

gentest("Virtual_Network_OSA_Query", "1",
        target=ADMIN)
quit()
gentest("Image_Deactivate", "1",
        target=PING,
        force_time="immed")

gentest("Image_Delete_DM", "1",
        target=PING,
        data_security_erase=smapi.Image_Delete_DM.NOERASE)

gentest("Image_Deactivate", None,
        target=PONG,
        force_time="immed")

gentest("Image_Delete_DM", None,
        target=PONG,
        data_security_erase=smapi.Image_Delete_DM.NOERASE)


