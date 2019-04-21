#!/usr/bin/python3

# Copyright 2018-2019 Leland Lucius
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pysmapi.tester import *
import pysmapi as smapi

#smapi.set_debug(True)

start_server()

runtest("./tests/Asynchronous_Notification_Disable_DM/1.test")
runtest("./tests/Asynchronous_Notification_Enable_DM/1.test")
runtest("./tests/Asynchronous_Notification_Query_DM/1.test")
runtest("./tests/Authorization_List_Add/1.test")
runtest("./tests/Authorization_List_Query/1.test")
runtest("./tests/Authorization_List_Remove/1.test")
runtest("./tests/Delete_ABEND_Dump/1.test")
runtest("./tests/Directory_Manager_Local_Tag_Define_DM/1.test")
runtest("./tests/Directory_Manager_Local_Tag_Delete_DM/1.test")
runtest("./tests/Directory_Manager_Local_Tag_Query_DM/1.test")
runtest("./tests/Directory_Manager_Local_Tag_Set_DM/1.test")
runtest("./tests/Directory_Manager_Search_DM/1.test")
runtest("./tests/Directory_Manager_Task_Cancel_DM/1.test")
runtest("./tests/Image_Activate/1.test")
runtest("./tests/Image_Active_Configuration_Query/1.test")
runtest("./tests/Image_CPU_Define/1.test")
runtest("./tests/Image_CPU_Define_DM/1.test")
runtest("./tests/Image_CPU_Delete/1.test")
runtest("./tests/Image_CPU_Delete_DM/1.test")
runtest("./tests/Image_CPU_Query/1.test")
runtest("./tests/Image_CPU_Query_DM/1.test")
runtest("./tests/Image_CPU_Set_Maximum_DM/1.test")
runtest("./tests/Image_Console_Get/1.test")
runtest("./tests/Image_Create_DM/1.test")
runtest("./tests/Image_Deactivate/1.test")
runtest("./tests/Image_Definition_Async_Updates/1.test")
runtest("./tests/Image_Definition_Create_DM/1.test")
runtest("./tests/Image_Definition_Create_DM/2.test")
runtest("./tests/Image_Definition_Delete_DM/1.test")
runtest("./tests/Image_Definition_Delete_DM/2.test")
runtest("./tests/Image_Definition_Delete_DM/3.test")
runtest("./tests/Image_Definition_Query_DM/1.test")
runtest("./tests/Image_Definition_Query_DM/2.test")
runtest("./tests/Image_Definition_Query_DM/3.test")
runtest("./tests/Image_Definition_Update_DM/1.test")
runtest("./tests/Image_Definition_Update_DM/2.test")
runtest("./tests/Image_Definition_Update_DM/3.test")
runtest("./tests/Image_Delete_DM/1.test")
runtest("./tests/Image_Device_Dedicate/1.test")
runtest("./tests/Image_Device_Dedicate_DM/1.test")
runtest("./tests/Image_Device_Reset/1.test")
runtest("./tests/Image_Device_Undedicate/1.test")
runtest("./tests/Image_Device_Undedicate_DM/1.test")
runtest("./tests/Image_Disk_Copy/1.test")
runtest("./tests/Image_Disk_Copy_DM/1.test")
runtest("./tests/Image_Disk_Create/1.test")
runtest("./tests/Image_Disk_Create_DM/1.test")
runtest("./tests/Image_Disk_Delete/1.test")
runtest("./tests/Image_Disk_Delete_DM/1.test")
runtest("./tests/Image_Disk_Query/1.test")
runtest("./tests/Image_Disk_Share/1.test")
runtest("./tests/Image_Disk_Share_DM/1.test")
runtest("./tests/Image_Disk_Unshare/1.test")
runtest("./tests/Image_Disk_Unshare_DM/1.test")
runtest("./tests/Image_IPL_Delete_DM/1.test")
runtest("./tests/Image_IPL_Query_DM/1.test")
runtest("./tests/Image_IPL_Set_DM/1.test")
runtest("./tests/Image_Lock_DM/1.test")
runtest("./tests/Image_Lock_Query_DM/1.test")
runtest("./tests/Image_MDISK_Link_Query/1.test")
runtest("./tests/Image_Name_Query_DM/1.test")
runtest("./tests/Image_Password_Set_DM/1.test")
runtest("./tests/Image_Pause/1.test")
runtest("./tests/Image_Query_Activate_Time/1.test")
runtest("./tests/Image_Query_DM/1.test")
runtest("./tests/Image_Recycle/1.test")
runtest("./tests/Image_Replace_DM/1.test")
runtest("./tests/Image_SCSI_Characteristics_Define_DM/1.test")
runtest("./tests/Image_SCSI_Characteristics_Query_DM/1.test")
runtest("./tests/Image_Status_Query/1.test")
runtest("./tests/Image_Unlock_DM/1.test")
runtest("./tests/Image_Volume_Add/1.test")
runtest("./tests/Image_Volume_Delete/1.test")
runtest("./tests/Image_Volume_Share/1.test")
runtest("./tests/Image_Volume_Space_Define_DM/1.test")
runtest("./tests/Image_Volume_Space_Define_DM/2.test")
runtest("./tests/Image_Volume_Space_Define_Extended_DM/1.test")
runtest("./tests/Image_Volume_Space_Define_Extended_DM/2.test")
runtest("./tests/Image_Volume_Space_Define_Extended_DM/3.test")
runtest("./tests/Image_Volume_Space_Query_DM/1.test")
runtest("./tests/Image_Volume_Space_Query_Extended_DM/1.test")
runtest("./tests/Image_Volume_Space_Remove_DM/1.test")
runtest("./tests/Image_Volume_Space_Remove_DM/2.test")
runtest("./tests/Image_Volume_Space_Remove_DM/3.test")
runtest("./tests/Image_Volume_Space_Remove_DM/4.test")
runtest("./tests/Metadata_Get/1.test")
runtest("./tests/Metadata_Get/2.test")
runtest("./tests/Metadata_Set/1.test")
runtest("./tests/Metadata_Space_Query/1.test")
runtest("./tests/Name_List_Add/1.test")
runtest("./tests/Name_List_Destroy/1.test")
runtest("./tests/Name_List_Query/1.test")
runtest("./tests/Name_List_Remove/1.test")
runtest("./tests/Network_IP_Interface_Create/1.test")
runtest("./tests/Network_IP_Interface_Modify/1.test")
runtest("./tests/Network_IP_Interface_Query/1.test")
runtest("./tests/Network_IP_Interface_Remove/1.test")
runtest("./tests/Page_or_Spool_Volume_Add/1.test")
runtest("./tests/Process_ABEND_Dump/1.test")
runtest("./tests/Query_ABEND_Dump/1.test")
runtest("./tests/Query_All_DM/1.test")
runtest("./tests/Query_All_DM/2.test")
runtest("./tests/Query_Asynchronous_Operation_DM/1.test")
runtest("./tests/Response_Recovery/1.test")
runtest("./tests/Shared_Memory_Access_Add_DM/1.test")
runtest("./tests/Shared_Memory_Access_Query_DM/1.test")
runtest("./tests/Shared_Memory_Access_Remove_DM/1.test")
runtest("./tests/Shared_Memory_Create/1.test")
runtest("./tests/Shared_Memory_Delete/1.test")
runtest("./tests/Shared_Memory_Query/1.test")
runtest("./tests/Shared_Memory_Replace/1.test")
runtest("./tests/System_Disk_IO_Query/1.test")
runtest("./tests/System_Disk_Query/1.test")
runtest("./tests/System_EQID_Query/1.test")
runtest("./tests/System_EQID_Query/2.test")
runtest("./tests/System_EQID_Query/3.test")
runtest("./tests/System_EQID_Query/4.test")
runtest("./tests/System_FCP_Free_Query/1.test")
runtest("./tests/System_Information_Query/1.test")
runtest("./tests/System_Page_Utilization_Query/1.test")
runtest("./tests/System_Performance_Information_Query/1.test")
runtest("./tests/System_Performance_Threshold_Disable/1.test")
runtest("./tests/System_Performance_Threshold_Enable/1.test")
runtest("./tests/System_RDR_File_Manage/1.test")
runtest("./tests/System_RDR_File_Query/1.test")
runtest("./tests/System_SCSI_Disk_Add/1.test")
runtest("./tests/System_SCSI_Disk_Delete/1.test")
runtest("./tests/System_SCSI_Disk_Query/1.test")
runtest("./tests/System_Service_Query/1.test")
runtest("./tests/System_Spool_Utilization_Query/1.test")
runtest("./tests/VMRELOCATE/1.test")
runtest("./tests/VMRELOCATE/2.test")
runtest("./tests/VMRELOCATE/3.test")
runtest("./tests/VMRELOCATE_Image_Attributes/1.test")
runtest("./tests/VMRELOCATE_Modify/1.test")
runtest("./tests/VMRELOCATE_Status/1.test")
runtest("./tests/VMRM_Configuration_Query/1.test")
runtest("./tests/VMRM_Configuration_Update/1.test")
runtest("./tests/VMRM_Measurement_Query/1.test")
runtest("./tests/Virtual_Channel_Connection_Create/1.test")
runtest("./tests/Virtual_Channel_Connection_Create_DM/1.test")
runtest("./tests/Virtual_Channel_Connection_Delete/1.test")
runtest("./tests/Virtual_Channel_Connection_Delete_DM/1.test")
runtest("./tests/Virtual_Network_Adapter_Connect_LAN/1.test")
runtest("./tests/Virtual_Network_Adapter_Connect_LAN_DM/1.test")
runtest("./tests/Virtual_Network_Adapter_Connect_Vswitch/1.test")
runtest("./tests/Virtual_Network_Adapter_Connect_Vswitch_DM/1.test")
runtest("./tests/Virtual_Network_Adapter_Connect_Vswitch_Extended/1.test")
runtest("./tests/Virtual_Network_Adapter_Create/1.test")
runtest("./tests/Virtual_Network_Adapter_Create_DM/1.test")
runtest("./tests/Virtual_Network_Adapter_Create_Extended/1.test")
runtest("./tests/Virtual_Network_Adapter_Create_Extended_DM/1.test")
runtest("./tests/Virtual_Network_Adapter_Delete/1.test")
runtest("./tests/Virtual_Network_Adapter_Delete_DM/1.test")
runtest("./tests/Virtual_Network_Adapter_Disconnect/1.test")
runtest("./tests/Virtual_Network_Adapter_Disconnect_DM/1.test")
runtest("./tests/Virtual_Network_Adapter_Query/1.test")
runtest("./tests/Virtual_Network_Adapter_Query_Extended/1.test")
runtest("./tests/Virtual_Network_LAN_Access/1.test")
runtest("./tests/Virtual_Network_LAN_Access_Query/1.test")
runtest("./tests/Virtual_Network_LAN_Create/1.test")
runtest("./tests/Virtual_Network_LAN_Delete/1.test")
runtest("./tests/Virtual_Network_LAN_Query/1.test")
runtest("./tests/Virtual_Network_OSA_Query/1.test")
runtest("./tests/Virtual_Network_VLAN_Query_Stats/1.test")
runtest("./tests/Virtual_Network_Vswitch_Create/1.test")
runtest("./tests/Virtual_Network_Vswitch_Create_Extended/1.test")
runtest("./tests/Virtual_Network_Vswitch_Create_Extended/2.test")
runtest("./tests/Virtual_Network_Vswitch_Create_Extended/3.test")
runtest("./tests/Virtual_Network_Vswitch_Delete/1.test")
runtest("./tests/Virtual_Network_Vswitch_Delete_Extended/1.test")
runtest("./tests/Virtual_Network_Vswitch_Query/1.test")
runtest("./tests/Virtual_Network_Vswitch_Query_Byte_Stats/1.test")
runtest("./tests/Virtual_Network_Vswitch_Query_Extended/1.test")
runtest("./tests/Virtual_Network_Vswitch_Query_Stats/1.test")
runtest("./tests/Virtual_Network_Vswitch_Set/1.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/1.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/10.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/11.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/12.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/13.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/14.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/15.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/16.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/17.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/18.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/19.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/2.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/20.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/21.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/22.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/23.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/3.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/4.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/5.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/6.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/7.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/8.test")
runtest("./tests/Virtual_Network_Vswitch_Set_Extended/9.test")
