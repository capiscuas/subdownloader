#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# generated by wxGlade 0.4.1 on Tue Feb 20 15:50:25 2007

import wx
import globals

import webbrowser
from xmlrpclib import Transport,Server
import  wx.lib.buttons  as  buttons
import  cStringIO
import os
import re
import SubDownloaderFrame
import struct

import extra.LabelBook.LabelBook as LB
from extra.LabelBook.Resources import *
from extra.AdvancedSplash import AdvancedSplash as AS
import thread
import threading
import  time

import gzip
import RecursiveParser
import  images
import SearchWindow

import SaveasReplaceDialog

import IMDBSearch
import locale
import pickle
import UpdateAlert
import platform
import base64
from extra.PyProgress import PyProgress as PP
from extra.CustomTreeCtrl import CustomTreeCtrl as CT

class PanelDownload(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PanelDownload.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
	
        self.list_downsubtitles = CT.CustomTreeCtrl(self, -1, pos=wx.DefaultPosition,style=wx.SUNKEN_BORDER,ctstyle=CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.static_line_1 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.button_browsefile = wx.Button(self, -1, _("Add video file"))
        self.button_browsedir = wx.Button(self, -1, _("Add directory"))
        self.button_clearlist = wx.Button(self, -1, _("Clear List"))
        self.button_downloadsub = wx.Button(self, -1, _("Download"))
        self.checkbox_checkall = wx.CheckBox(self, -1, _("Select / Unselect ALL"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
	

    def __set_properties(self):
        # begin wxGlade: PanelDownload.__set_properties
        self.button_browsedir.SetToolTipString(_("Add film's directory"))
        self.button_downloadsub.Enable(False)
        # end wxGlade

    def __do_layout(self):
	self.Initialize()
        # begin wxGlade: PanelDownload.__do_layout
        sizer_6_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.list_downsubtitles, 1, wx.EXPAND, 0)
        sizer_1.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_2.Add(self.button_browsefile, 0, wx.ALIGN_BOTTOM|wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.button_browsedir, 0, wx.ALIGN_BOTTOM|wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.button_clearlist, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add((0, 50), 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.button_downloadsub, 0, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_6_copy.Add(sizer_1, 1, wx.EXPAND, 0)
        sizer_7.Add(self.checkbox_checkall, 0, wx.ADJUST_MINSIZE, 0)
        sizer_7.Add((20, 0), 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer_6_copy.Add(sizer_7, 0, wx.EXPAND|wx.ALIGN_RIGHT, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_6_copy)
        sizer_6_copy.Fit(self)
        sizer_6_copy.SetSizeHints(self)
        # end wxGlade
        
    def Initialize(self):
	
	self.button_browsedir.Destroy()
        self.button_browsedir = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join(globals.sourcefolder,"images/buttons/open_folder.png"), wx.BITMAP_TYPE_ANY))
	self.button_browsedir.SetToolTipString(_("Add videos from folder (recursive)"))
	
	self.button_browsefile.Destroy()
        self.button_browsefile = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join(globals.sourcefolder,"images/buttons/open_video.png"), wx.BITMAP_TYPE_ANY))
	self.button_browsefile.SetToolTipString(_("Add video file"))

	self.button_downloadsub.Destroy()
        self.button_downloadsub = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join(globals.sourcefolder,"images/buttons/download.png"), wx.BITMAP_TYPE_ANY))
	self.button_downloadsub.SetToolTipString(_("Download Subtitles"))
	
	self.button_clearlist.Destroy()
        self.button_clearlist = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join(globals.sourcefolder,"images/buttons/clear.png"), wx.BITMAP_TYPE_ANY))
	self.button_clearlist.SetToolTipString(_("Clear content"))
	 
	self.Bind(wx.EVT_BUTTON, self.OnButtonBrowseFile, self.button_browsefile)
	self.Bind(wx.EVT_BUTTON, self.OnButtonBrowseDir, self.button_browsedir)
	self.Bind(wx.EVT_BUTTON, self.OnButtonDownloadSub, self.button_downloadsub)
	self.list_downsubtitles.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClickItem)
	self.Bind(wx.EVT_CHECKBOX, self.OnCheckAllTree, self.checkbox_checkall)
	self.Bind(wx.EVT_BUTTON, self.OnClearTree, self.button_clearlist)
	self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnSelTreeChanged, self.list_downsubtitles)
	
	self.table_videoitems_hashes = {}
	self.table_videoinfo_hashes = {}
	
	self.list_downsubtitles.DeleteAllItems()
	self.listvideofiles = []
	self.rootitem = self.list_downsubtitles.AddRoot("Video Files list")
	
	isz = (18,12)
	il = wx.ImageList(isz[0], isz[1])
	self.treeimage_video = il.Add(wx.ArtProvider_GetBitmap(wx.ART_EXECUTABLE_FILE,      wx.ART_OTHER, isz))
	self.treeimage_sub = il.Add(wx.ArtProvider_GetBitmap(wx.ART_HELP_SETTINGS,   wx.ART_OTHER, isz))
	self.flagsimages = {}
	self.list_selecteditems = []
	self.list_allsubtreeitems = []
	
	#Move this to SUBDOWNLOADER.py during the splash window
	parser = RecursiveParser.RecursiveParser()
	gif_flags = parser.getRecursiveFileList(os.path.join(globals.sourcefolder,'flags'), ['gif'])
	globals.flag_bitmaps = {}
	for gif_file in gif_flags:
		gifname = os.path.basename(gif_file)
		bitmap = wx.Bitmap(gif_file)
		language_name = gifname[:-4]
		
		if len(language_name) == 2:		
			globals.flag_bitmaps[language_name] = bitmap
			self.flagsimages[gifname] = il.Add(bitmap)
		
	self.il = il
	
	self.list_downsubtitles.SetImageList(il)
	self.list_downsubtitles.SetTreeStyle(CT.TR_HIDE_ROOT|CT.TR_NO_LINES)
    def OnDoubleClick(self,evt):
	item = evt.GetItem()
	if not self.list_downsubtitles.GetItemParent(item) == self.rootitem:
		self.OnButtonDownloadSub(wx.EVT_BUTTON)
	
    def OnRightClickItem(self,evt):
		self.item_choiced = evt.GetItem()

		if not self.list_downsubtitles.IsSelected(self.item_choiced):
			self.list_downsubtitles.SelectItem(self.item_choiced)
		
		if not hasattr(self, "firstpopup"):
			self.firstpopup = True
			self.PopupItemPlayAVIMplayer = wx.NewId()
			self.PopupItemPlayAVIVlc = wx.NewId()
			self.Bind(wx.EVT_MENU, self.OnButtonPlayAVIMplayer, id=self.PopupItemPlayAVIMplayer)
			self.Bind(wx.EVT_MENU, self.OnButtonPlayAVIVlc, id=self.PopupItemPlayAVIVlc)
			self.PopupItemSearchVideoFile = wx.NewId()
			self.Bind(wx.EVT_MENU, self.OnButtonSearchVideoFile, id=self.PopupItemSearchVideoFile)
			self.PopupItemViewIMDBDetails = wx.NewId()
			self.Bind(wx.EVT_MENU, self.OnButtonSeeIMDBDetails, id=self.PopupItemViewIMDBDetails)
			
			self.PopupItemDownload = wx.NewId()
			self.Bind(wx.EVT_MENU, self.OnButtonDownloadSub, id=self.PopupItemDownload)
			self.PopupItemReportBadSub = wx.NewId()
			self.Bind(wx.EVT_MENU, self.OnReportBadInfo, id=self.PopupItemReportBadSub)
			self.PopupItemViewDetailsWeb = wx.NewId()
			self.Bind(wx.EVT_MENU, self.OnViewDetailsWeb, id=self.PopupItemViewDetailsWeb)
			self.PopupItemReportBadTitle = wx.NewId()
			self.Bind(wx.EVT_MENU, self.OnReportBadTitle, id=self.PopupItemReportBadTitle)
			self.PopupItemReportBadLanguage = wx.NewId()
			self.Bind(wx.EVT_MENU, self.OnReportBadLanguage, id=self.PopupItemReportBadLanguage)
			self.PopupItemReport = wx.NewId()
			
		if self.list_downsubtitles.GetItemParent(self.item_choiced) != self.rootitem:
			
			MyPopupMenu = wx.Menu()
			MyPopupMenu.Append(self.PopupItemDownload, _("Download subtitle"))
			MyPopupMenu.Append(self.PopupItemViewDetailsWeb, _("View Details and Rate Subtitle"))
			
			ReportSubMenu = wx.Menu()
			ReportSubMenu.Append(self.PopupItemReportBadSub, _("This SUBTITLE is not for this AVI"))
			ReportSubMenu.Append(self.PopupItemReportBadTitle, _("The MOVIE IMDB is not for this AVI"))
			ReportSubMenu.Append(self.PopupItemReportBadLanguage, _("The subtitle LANGUAGE is not correct"))
			MyPopupMenu.AppendMenu(self.PopupItemReport, _("Report us Wrong Info"),ReportSubMenu)
			
			VideoMenu = wx.Menu()
			if globals.preferences_list.has_key("mplayer"):
			    VideoMenu.Append(self.PopupItemPlayAVIMplayer, _("Mplayer"))
			if globals.preferences_list.has_key("vlc"):
			    VideoMenu.Append(self.PopupItemPlayAVIVlc, _("VLC"))
			MyPopupMenu.AppendMenu(self.PopupItemPlayAVIMplayer,_("Play With"),VideoMenu)
			
			pos = self.ScreenToClient(wx.GetMousePosition())
			self.PopupMenu(MyPopupMenu, pos)
			MyPopupMenu.Destroy()
		else:
		    
			#The videofile item
			MyPopupMenu = wx.Menu()
			item_data = self.list_downsubtitles.GetPyData(self.item_choiced)
			if item_data.has_key("IDMovieImdb"):
			    MyPopupMenu.Append(self.PopupItemViewIMDBDetails, _("IMDB details"))
			MyPopupMenu.Append(self.PopupItemSearchVideoFile, _("Find other subs of this Movie on the web"))
			pos = self.ScreenToClient(wx.GetMousePosition())
			self.PopupMenu(MyPopupMenu, pos)
			MyPopupMenu.Destroy()
		
    def OnButtonPlayAVIMplayer(self,evt):
	"""Plays the Movie from the subdownloader itself with the 
	selected subtitle.
	
	Thanks for mplayer and vlc developing team
	"""
	
	if not globals.preferences_list.has_key("mplayer") or not os.path.exists(globals.preferences_list["mplayer"]):
	    wx.MessageBox(_("%s executable not found. \nYou need to set up the path from (%s -> %s)") % ("Mplayer",_("Options"),_("Misc")))
	    return
	
	sub_data = self.list_downsubtitles.GetPyData(self.item_choiced)
	video_data = self.list_downsubtitles.GetPyData(self.list_downsubtitles.GetItemParent(self.item_choiced))
	video_filename = os.path.join(video_data["dirname"],video_data["filename"])
	subfile_id = sub_data["IDSubtitleFile"]	
	# We learn about the users system, and use the correct file settings(next 5 lines)
	win = re.compile('nt')
	if win.match(os.name):
		path_sub_temp = os.path.join(globals.sourcefolder,"conf","temp.srt")
	else:
		path_sub_temp = os.path.join(globals.sourcefolder,sub_data.get("subname"))
	self.download_dlg = PP.PyProgress(None, -1, _("Downloading"),
                            _("Downloading, it can take a while..."),                            
                            style = wx.PD_CAN_ABORT)
	
	self.DownloadSubtitle(subfile_id,path_sub_temp)
	self.download_dlg.Destroy()
	executable = globals.preferences_list["mplayer"]
	try:
	    executable_quote = '"' + executable+'"'
	    win = re.compile('nt')
	    if win.match(os.name):
		    os.spawnve(os.P_NOWAIT, executable,[executable_quote,'"'+video_filename+'"' + ' -sub "'+path_sub_temp+'"'], os.environ)
	    else:
		    os.spawnve(os.P_NOWAIT, executable,[executable_quote,video_filename,"-sub",path_sub_temp], os.environ)
	except AttributeError:
	    pid = os.fork()
	    if not pid :
		os.execvpe(executable,[executable_quote,video_filename + ' -sub "'+path_sub_temp+'"'],os.environ)
	except:
	    wx.MessageBox("The path that you specified is wrong")

	#End of OnButtonPlayAVI
			
	
    def OnButtonPlayAVIVlc(self,evt):
	"""Plays the Movie from the subdownloader itself with the 
	selected subtitle.
	
	Thanks for mplayer and vlc developing team
	"""
	if not globals.preferences_list.has_key("vlc") or not os.path.exists(globals.preferences_list["vlc"]):
	    wx.MessageBox(_("%s executable not found. \nYou need to set up the path from (%s -> %s)") % ("VLC",_("Options"),_("Misc")))
	    return
	sub_data = self.list_downsubtitles.GetPyData(self.item_choiced)
	video_data = self.list_downsubtitles.GetPyData(self.list_downsubtitles.GetItemParent(self.item_choiced))
	video_filename = os.path.join(video_data["dirname"],video_data["filename"])
	subfile_id = sub_data["IDSubtitleFile"]	
	
	win = re.compile('nt')
	if win.match(os.name):
		path_sub_temp = os.path.join(globals.sourcefolder,"conf","temp.srt")
	else:
		path_sub_temp = os.path.join(globals.sourcefolder,sub_data.get("subname"))
	self.download_dlg = PP.PyProgress(None, -1, _("Downloading"),
                            _("Downloading, it can take a while..."),                            
                            style = wx.PD_CAN_ABORT)
	self.DownloadSubtitle(subfile_id,path_sub_temp)
	self.download_dlg.Destroy()
	
	executable = globals.preferences_list["vlc"]
	try:
	    executable_quote = '"' + executable+'"'
	    win = re.compile('nt')
	    if win.match(os.name):
		    os.spawnve(os.P_NOWAIT, executable,[executable_quote,video_filename + ' --sub-file "'+path_sub_temp+'"'], os.environ)
	    else:
		    os.spawnve(os.P_NOWAIT, executable,[executable_quote,video_filename,' --sub-file ',path_sub_temp], os.environ)
	except AttributeError:
	    pid = os.fork()
	    if not pid :
		os.execvpe(executable,[executable_quote,video_filename + ' --sub-file "'+path_sub_temp+'"'],os.environ)
	except:
	    wx.MessageBox("The path that you specified is wrong")
	
	    
	#End of OnButtonPlayAVIVlc
			

    def OnButtonSearchVideoFile(self,evt):
		item_data = self.list_downsubtitles.GetPyData(self.item_choiced)
		if item_data.has_key("IDMovie"):
			link = globals.MakeOSLink("search/idmovie-" + str(item_data["IDMovie"]))
		else:
			link = globals.MakeOSLink("search2/sublanguageid-all/moviename-" + str(item_data["filename"].encode("ascii",'ignore')))
		try:
			webbrowser.open(link)
		except:
			msg = _("Error opening link")
			wx.MessageBox(msg + " " + link)
			
    def OnButtonSeeIMDBDetails(self,evt):
		item_data = self.list_downsubtitles.GetPyData(self.item_choiced)
		link = "http://www.imdb.com/title/tt" + str(item_data["IDMovieImdb"]) + "/"
		
		try:
			webbrowser.open(link)
		except:
			msg = _("Error opening link")
			wx.MessageBox(msg + " " + link)
			
    def OnViewDetailsWeb(self,evt):
		item_data = self.list_downsubtitles.GetPyData(self.item_choiced)
		idsubtitle = item_data["idsubtitle"]
		try:
			webbrowser.open(globals.MakeOSLink("subtitles/" + str(idsubtitle)))
		except:
			msg = _("Error opening link")
			wx.MessageBox(msg +" "+ globals.MakeOSLink("subtitles/" + str(idsubtitle)))
		    
			
    def OnReportBadTitle(self,evt):
		item_data = self.list_downsubtitles.GetPyData(self.item_choiced)
		idsubtitle = item_data["idsubtitle"]
		try:
			webbrowser.open(globals.MakeOSLink("report/idsubtitle-" + str(idsubtitle)))
		except:
			msg = _("Error opening link")
			wx.MessageBox(msg +" "+ globals.MakeOSLink("report/idsubtitle-" + str(idsubtitle)))
			
    def OnReportBadLanguage(self,evt):
		item_data = self.list_downsubtitles.GetPyData(self.item_choiced)
		idsubtitle = item_data["idsubtitle"]
		try:
			webbrowser.open(globals.MakeOSLink("report/idsubtitle-" + str(idsubtitle)))
		except:
			msg = _("Error opening link")
			wx.MessageBox(msg +" "+ globals.MakeOSLink("report/idsubtitle-" + str(idsubtitle)))
			
    def OnReportBadInfo(self,evt):
		item_data = self.list_downsubtitles.GetPyData(self.item_choiced)
		IDSubMovieFile = item_data["IDSubMovieFile"]
		dlg = wx.MessageDialog(
				None,
				_("Are you sure these subtitles are not good for your video file?") + "\n" + _("(It means subtitles are for this movie, but are not well-synchronized)"),
				"Reporting bad HASH",
				wx.YES_NO | wx.ICON_QUESTION 
				)
		userChoice = dlg.ShowModal()
		if userChoice == wx.ID_YES:
			try:
				answer = globals.xmlrpc_server.ReportWrongMovieHash(globals.osdb_token,IDSubMovieFile)
				wx.MessageBox(_("The report has been noted. Thank you very much."))
			except:
				wx.MessageBox("Error in method XMLRPC Report Bad hash")
	
    def OnButtonBrowseFile(self,event):
		dlg = wx.FileDialog(
			self, message=_("Browse video..."), defaultDir=globals.preferences_list["cwd"], 
			defaultFile="", wildcard=globals.videos_wildcards, style=wx.OPEN |wx.CHANGE_DIR)
	
			
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			globals.preferences_list["cwd"] = os.path.dirname(path)
			self.AddVideo([path])
			self.OnButtonSearch(wx.EVT_BUTTON)
			
			#self.list_downsubtitles.ExpandAll(self.rootitem)
			#self.list_downsubtitles.Refresh()
			
		dlg.Destroy()
		

    def OnButtonBrowseDir(self,event):
		dlg = wx.DirDialog(self, _("Choose directory..."),style=wx.DD_DEFAULT_STYLE)
		dlg.SetPath(globals.preferences_list["cwd"])
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			globals.preferences_list["cwd"] = dlg.GetPath()
			self.AddVideo([path])
			self.OnButtonSearch(wx.EVT_BUTTON)
		dlg.Destroy()
			
	
						
    def OnButtonDownloadSub(self,event):
		self.thread_canceled = False
		selections = self.list_downsubtitles.GetSelections()
		self.thread_opensaveaswindow = False
		
		exit = False
		maximum = 10
		self.download_dlg = PP.PyProgress(None, -1, _("Downloading"),
                            _("Downloading, it can take a while..."),                            
                            style = wx.PD_CAN_ABORT)
		
		self.download_dlg.CenterOnParent()
		wx.YieldIfNeeded()
		
		self.SearchKeepGoing = True
		self.has_been_errors = False    
		
		wx.BeginBusyCursor()
		
		self.download_subs = 0
		total_downloads = len(self.list_selecteditems)
		for dwn_counter,selection in enumerate(self.list_selecteditems):
			if not self.SearchKeepGoing:
				self.thread_canceled = True
				wx.EndBusyCursor()
				return
				
				
			data = self.list_downsubtitles.GetPyData(selection)
			data_parent = self.list_downsubtitles.GetPyData(self.list_downsubtitles.GetItemParent(selection))  #We get the movie file info
			
			subname = data["subname"]
			dirname = data["dirname"]
			sublang = data["lang"]

			videoname = data_parent["filename"]
			total_lang = len(data_parent["sons_lang"])
			
			lastpointposition = subname.rfind(".")
			subtitle_ext = subname[lastpointposition+1:]
			
			lastpointposition = videoname.rfind(".")
			if total_lang > 1:
				final_subname = videoname[:lastpointposition] + "." + sublang + "." + subtitle_ext
			else:
				final_subname = videoname[:lastpointposition] + "." + sublang + "." + subtitle_ext
					
			if globals.preferences_list["download_radio1"] == False:
				dirname = globals.preferences_list["download_folder"]

			destinationpath = os.path.join(dirname,final_subname)
			IDSubtitleFile = data["IDSubtitleFile"]
			
			if os.path.exists(destinationpath):
			    savedlg = SaveasReplaceDialog.SaveasReplaceDialog(_("The file %s already exists.\nDo you want to replace it?") % destinationpath,
				    self,-1,"Replace file",  style = wx.YES_NO| wx.ICON_INFORMATION
				    )
			    
			    savedlg.CenterOnParent()
			    self.userChoice = savedlg.ShowModal()
	    
			    if self.userChoice == wx.ID_CANCEL:
				    continue
			    elif self.userChoice == wx.ID_SAVEAS: #He choosed to SAVE AS
				    saveas_dlg = wx.FileDialog(
					    self, message=_("Save as..."), defaultDir=globals.preferences_list["cwd"], 
					    defaultFile=final_subname, style=wx.SAVE |wx.OVERWRITE_PROMPT
					    )
				    
				    if saveas_dlg.ShowModal() == wx.ID_OK:
					    dest = saveas_dlg.GetPath()
					    saveas_dlg.Destroy()
				    else:
					    saveas_dlg.Destroy()
					    continue
		
			self.DownloadDialogMessage = _("Downloading subtitle %s of %s") % (str(dwn_counter+1),str(total_downloads))
			self.SearchKeepGoing = self.download_dlg.UpdatePulse (self.DownloadDialogMessage)
			self.DownloadSubtitle(IDSubtitleFile,destinationpath)
		
		self.download_dlg.Destroy()
		wx.EndBusyCursor()
		
		self.thread_canceled = True #We want to close de dialog
		
		lines = ""
		count = 0

		if total_downloads:    
		    text_label = _("%d subtitle(s) were downloaded") % self.download_subs
		    if self.has_been_errors:	
			    text_label += "\n" + _("Some errors found:") + "\n" + self.text_logmessages
		    wx.MessageBox(text_label)

    def DownloadSubtitle(self,sub_id,dest = "temp.sub"):

	try:
		subtitlefile = file(dest,'wb')
		subtitlefile.close()
	except:
		self.LogMessage("Error saving " + dest)
		return
		
	if globals.debugmode:
		globals.Log("-------------Download parameters:")
		globals.Log([sub_id])
		
	try:
		answer = globals.xmlrpc_server.DownloadSubtitles(globals.osdb_token,[sub_id])
		if globals.debugmode:
			globals.Log("-------------Download Answer:")
			globals.Log("disabled")
		
		if answer.has_key("data"):
			subtitle_compressed = answer["data"][0]["data"]
		else:
			self.LogMessage("XMLRPC Error downloading result for idsubfile="+sub_id)
			
		compressedstream = base64.decodestring(subtitle_compressed)
		#compressedstream = subtitle_compressed
							
		import StringIO
		gzipper = gzip.GzipFile(fileobj=StringIO.StringIO(compressedstream))
		
		s=gzipper.read()
		gzipper.close()
		subtitlefile = file(dest,'wb')
		subtitlefile.write(s)
		subtitlefile.close()
		self.LogMessage(dest + " saved",status="OK")
		self.download_subs +=1
	except: 
		self.LogMessage("XMLRPC Error downloading id="+sub_id)
		
	
				
    def OnButtonSearch(self,event):
		
		self.has_been_errors = False    
			
		self.thread_canceled = False
		self.SearchKeepGoing = True
		
		exit = False
		maximum = 10
		
		self.searchdlg = PP.PyProgress(None, -1, _("Search Progress"),
                            _("Searching..."),                            
                            style = wx.PD_CAN_ABORT)
		
		
		self.SearchDialogMessage = ""
		self.total_subs_found = -1
		self.list_allsubtreeitems = []
		self.list_selecteditems = []
		self.button_downloadsub.Disable()

		self.searchdlg.CenterOnParent()
		wx.BeginBusyCursor()
		
		
		listdown = self.list_downsubtitles
		self.SearchDialogMessage = _("Searching...")
		count = 0
		self.SearchKeepGoing = self.searchdlg.UpdatePulse(self.SearchDialogMessage)
		if not self.SearchKeepGoing:
			self.thread_canceled = True
			wx.EndBusyCursor()
			return

		total_subs_found = 0
		totalfiles = len(self.listvideofiles)
		
			
		#if totalfiles == 100:
			#wx.MessageBox("The maximum of subtitles searched is 100.")

		if totalfiles != 0 and not globals.disable_osdb:
		    #OPENSUBTITLES DATABASE SEARCH
		    
		    self.SearchDialogMessage = _("Searching using OSDB protocol")
		    if not globals.use_threads:
			    wx.YieldIfNeeded()		
		    searchlist = []
		    
		    #Searching only subtitles in this languages
		    langs_search = globals.preferences_list["search_langs"]
		    
		    listdown = self.list_downsubtitles
		    #listdown.DeleteAllItems()
		    for videofile in self.listvideofiles:
			    searchlist.append({'sublanguageid':langs_search,'moviehash':videofile["hashresults"]["hash"],'moviebytesize':str(videofile["hashresults"]["filesize"])})

		    if globals.debugmode:
			    globals.Log("-------------Sending parameters:")
			    globals.Log(searchlist)
			    
		    results = {'data':False} #If SearchSubtitles fails, doesn't make bug.
		    self.SearchKeepGoing = self.searchdlg.UpdatePulse(_("Searching, it can take a while..."))
		    if not self.SearchKeepGoing:
			self.thread_canceled = True
			wx.EndBusyCursor()
			return
		    
		    try:
			    results = globals.xmlrpc_server.SearchSubtitles(globals.osdb_token,searchlist)
			    error_osdb = False
		    except:
			    error = _("Error connecting to the OSDB server")
			    globals.Log(error)
			    wx.MessageBox(error)
			    error_osdb = True
		    
		    sons_lang = []
		    if not error_osdb:
			    if not globals.use_threads:
				    wx.YieldIfNeeded()
			    if globals.debugmode:
				    globals.Log("-------------Received:")
				    globals.Log(results)
			    if not results['data'] == False:
				    for subtitle in results['data']:
					    if not self.SearchKeepGoing:
						    self.thread_canceled = True
						    wx.EndBusyCursor()
						    return
					    total_subs_found += 1
					    videoitem = self.table_videoitems_hashes[subtitle["MovieHash"]]
					    videoinfo = self.table_videoinfo_hashes[subtitle["MovieHash"]]
					    listdown.SetItemBold(videoitem)
					    
					    lang = subtitle["ISO639"]
					    if not lang in sons_lang:
						    sons_lang.append(lang)
					    
					    str_uploader = subtitle["UserNickName"]
					    if str_uploader == "":
						    str_uploader = _("Anonymous")
					    
					    subinfo = "["+ subtitle["LanguageName"] +"] " + subtitle["SubFileName"].encode("ascii",'replace')  \
							    +" [Rate: "+ subtitle["SubRating"] + "] Uploader: "+ str_uploader
					    
					    if subtitle["MovieNameEng"]:
						    text = "\"" + subtitle["MovieName"].encode("ascii",'replace')  + "\" aka \"" + subtitle["MovieNameEng"] + "\"" 
					    else:
						    text = "\"" + subtitle["MovieName"].encode("ascii",'replace') + "\"" 
					    
					    text+= " [IMDB "+subtitle["IDMovieImdb"] + "]   file=" + videoinfo["filename"]
					    listdown.SetItemText(videoitem,text)
					    listdown.SetPyData(videoitem,{"IDMovieImdb":subtitle["IDMovieImdb"],"IDMovie":subtitle["IDMovie"],"filename":videoinfo["filename"],"sons_lang":sons_lang,
									  "dirname":videoinfo["dirname"]})
						    
					    subitem = listdown.AppendItem(videoitem,subinfo,ct_type= 1)
					    self.list_allsubtreeitems.append(subitem)
					    listdown.Expand(videoitem)
					    #self.dlg.link_already.SetURL(globals.MakeOSLink("search/sublanguageid-all/imdbid-"+ subtitle["IDMovieImdb"]))
					    gifname = lang + ".gif"
					    if self.flagsimages.has_key(gifname):
						    listdown.SetItemImage(subitem, self.flagsimages[gifname], wx.TreeItemIcon_Normal)
					    else:
						    listdown.SetItemImage(subitem, self.treeimage_sub, wx.TreeItemIcon_Normal)
					    #listdown.SetItemTextColour(subitem, wx.RED)
					    listdown.SetPyData(subitem, {"protocol":"osdb","idsubtitle":subtitle["IDSubtitle"],"subname":subtitle["SubFileName"],
									 "dirname":videoinfo["dirname"],"lang":lang,"IDSubtitleFile":subtitle["IDSubtitleFile"],
									 "IDSubMovieFile":subtitle["IDSubMovieFile"]})
			    
    
			    if not self.SearchKeepGoing:
				    self.thread_canceled = True
				    wx.EndBusyCursor()
				    return
		wx.YieldIfNeeded()
		
		wx.EndBusyCursor()


		#self.dlg.button_cancel.SetLabel("Close")
		#self.dlg.gauge.SetValue(self.dlg.gauge.GetRange())
		#self.dlg.label_function.SetLabel("Finished:")
		
		self.total_subs_found = total_subs_found
		self.thread_canceled = True

		
		lines = ""
		count = 0
		go_up = True

			 
		self.searchdlg.Destroy()
		
		if self.total_subs_found == 0 or self.has_been_errors:
			self.dlg = SearchWindow.SubWindow(self, -1, _("Searching..."), size=(350, 200),
					#style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME
					style = wx.DEFAULT_DIALOG_STYLE)

			self.dlg.ShowModal()
			
		if globals.update_list:
			update_dlg = UpdateAlert.MyDialog(globals.update_list,self, -1, _("New Version Detected"), size=(350, 200),
				#style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME
				style = wx.DEFAULT_DIALOG_STYLE)
			update_dlg.ShowModal()
			
		globals.update_list = {}
	
    def AddVideo(self,files):
		self.text_logmessages = ""
		self.has_been_errors = False
		list = []

		if globals.param_function == "--search":
			globals.param_function = ""
			ok = False
			no_connection = False
			if globals.disable_osdb:
				wx.BusyInfo(_("Connecting to server..."))
				count = 0
		
				while True:
				    wx.MilliSleep(10)
				    count += 1
				    if count == 600:
					no_connection = True
					break
					

			files = []
			for shortfilename in globals.param_files:
				try:
					file_name = unicode(win32api.GetLongPathName(shortfilename))
				except:
					file_name = shortfilename
				globals.Log("Enqueing file = " + file_name)
				files.append(file_name)
		
		self.hashing_dlg = PP.PyProgress(None, -1, _("Calculating Hash"),
                            _("Hashing files..."),                            
                            style = wx.PD_CAN_ABORT)
		for file in files:
			if os.path.isdir(file):
				dir = file
				parser = RecursiveParser.RecursiveParser()
				recursivefiles = parser.getRecursiveFileList(dir, globals.videos_ext)
				list.extend(recursivefiles)
			elif os.path.isfile(file):
				list.append(file)
			else:
				wx.MessageBox(file +" is not a valid file or folder.")
				return
			    
		
			
		for file in list:		    
		    
			file_name = globals.EncodeLocale(os.path.basename(file))
			self.SearchKeepGoing = self.hashing_dlg.UpdatePulse(file_name)
			if not self.SearchKeepGoing:
				self.thread_canceled = True
				self.hashing_dlg.Destroy()
				return	
			    
			hashresult = globals.getAddress(file)
			if hashresult == "IOError":
				self.LogMessage(_("Found error in the file %s") % file)
				continue
			elif hashresult == "SizeError":
				self.LogMessage(_("Size error in the file %s") % file)
				continue
			elif hashresult == "NotFoundError":
				self.LogMessage(_("The file <%s> can't be found") % file)
				continue
			else:
				
				videofile = {'file': file,'basename':os.path.basename(file),'dirname':os.path.dirname(file),'filename':hashresult['filename'],'hashresults':hashresult}
				
				listdown = self.list_downsubtitles
				
				videoinfo = videofile["basename"] + " "*7 + videofile["dirname"]
				videoitem = listdown.AppendItem(self.rootitem, videoinfo)

				listdown.SetItemImage(videoitem, self.treeimage_video, wx.TreeItemIcon_Normal)
				listdown.SetPyData(videoitem,{"filename":videofile["basename"]})
				key = "" + videofile["hashresults"]["hash"]
				self.table_videoitems_hashes[key] = videoitem #For example "HASH1:treeitem1,HASH2:treeitem2"
				self.table_videoinfo_hashes[key] = videofile
				self.listvideofiles.append(videofile)

				
		self.hashing_dlg.Destroy()
		if self.has_been_errors:
		    wx.MessageBox(self.text_logmessages)
		    globals.Log(self.text_logmessages)
			
    def OnClearTree(self,event):
	self.list_downsubtitles.DeleteChildren(self.rootitem)
	
	self.list_selecteditems = []
	self.button_downloadsub.Disable()
	self.listvideofiles = []
	self.list_allsubtreeitems = []
	
	
    def OnCheckAllTree(self, event):
	
		for item in self.list_allsubtreeitems:
			if self.list_downsubtitles.GetItemBackgroundColour(item) != wx.NamedColour('WHEAT'):
				all_selected = False
				break
			
		if self.checkbox_checkall.IsChecked():
		    #We select all the subtitles
		    self.list_downsubtitles.CheckChilds(self.rootitem,True)
		    for item in self.list_allsubtreeitems:
			    self.list_downsubtitles.SetItemBackgroundColour(item,wx.NamedColour('WHEAT'))
			    if not item is self.list_selecteditems:
				    self.list_selecteditems.append(item)
				    
		    if len(self.list_allsubtreeitems):
			self.button_downloadsub.Enable()
		else:
		    self.list_downsubtitles.CheckChilds(self.rootitem,False)
		    self.list_downsubtitles.UnselectAll()
		    self.list_selecteditems = []
		    for item in self.list_allsubtreeitems:
			    self.list_downsubtitles.SetItemBackgroundColour(item,wx.WHITE)
		    self.button_downloadsub.Disable()

		
		self.Refresh()

    def LogMessage(self,message,status="ERROR"):
		if status == "ERROR":
			self.has_been_errors = True
		self.text_logmessages += message + "\n"
		
    def OnSelTreeChanged(self, event):
		
		item = event.GetItem()
		
		if item.IsOk():
			if self.list_downsubtitles.GetItemParent(item) == self.list_downsubtitles.GetRootItem():
				self.unselect = True
			else:
				self.unselect = False
				if not item in self.list_selecteditems:
					self.list_downsubtitles.SetItemBackgroundColour(item,wx.NamedColour('WHEAT'))
					self.list_selecteditems.append(item)
				else:
					self.list_downsubtitles.SetItemBackgroundColour(item,wx.WHITE)
					del self.list_selecteditems[self.list_selecteditems.index(item)]
					
	
		if   len(self.list_selecteditems) > 0:
			self.button_downloadsub.Enable()
		else:
			self.button_downloadsub.Disable()
		self.Refresh()

	
# end of class PanelDownload


