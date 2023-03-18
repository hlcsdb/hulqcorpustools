
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog as fd

from resources.constants import FileFormat, TransliterandFile
from transliterator import controller as tr


_workingdirectory = str(Path(__file__).parent)
_inputdir = _workingdirectory + '/input'
_outputdir = _workingdirectory + '/output'

#TODO: add hunquminumize switch both for sounds as well as words
# dg has been putting z in orthography (which is an sh in orthography
# phonologically) that should come out as x in APA

class SourceFileFrame(ttk.LabelFrame):
    def __init__(self, parent):
        self.source_file_section = ttk.LabelFrame.__init__(
                                        self,
                                        parent,
                                        text='Files')
        self.parent = parent
        self.source_file_list = parent.source_file_list

        # start treeview, handoff source_file_list
        self.treeview_frame = TreeviewFrame(self)
        self.file_list_view = self.treeview_frame.file_list_view
        
        self.source_button_row_frame = SourceButtonRow(self)

        self.treeview_frame.pack(side='top', fill='both', expand=True)
        self.source_button_row_frame.pack(fill='x', side='bottom')

    def add_files(self, add_file_list):
        """add files from find_file list or what have you to the list

        Arguments:
            add_file_list -- list of files
        """

        currently_added_files = {
            self.file_list_view.item(_file)['values'][0]
            for _file in self.file_list_view.get_children()
        }
        
        for _file in add_file_list:
            if _file not in currently_added_files:
                self.file_list_view.insert('',
                tk.END,
                values=(_file,))

        self.update_file_list()

    def update_file_list(self):
        '''retrieves the file list from the treeview and updates
        the globel source file list'''

        self.source_file_list.clear
        self.source_file_list.update({
            self.file_list_view.item(_file)['values'][0]
            for _file in self.file_list_view.get_children()})

        


class SourceButtonRow(ttk.Frame):
    def __init__(self, parent):
        self.button_row_frame = ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.file_list_view = parent.file_list_view
        
        self.make_file_source_buttons(self)

    def make_file_source_buttons(self, parent):
        '''assemble the button row with browse, remove, clear'''
        browse_button = ttk.Button(
                            parent,
                            text='Browse...',
                            command=self.find_files
                            )


        file_remove_button = ttk.Button(
                                parent,
                                text='Remove',
                                command=self.remove_files
                                )

        file_clear_button = ttk.Button(
                            parent,
                            text='Clear',
                            command=self.clear_files
                            )

        browse_button.pack(side='left')
        file_remove_button.pack(side='left')
        file_clear_button.pack(side='left')

    # file dialog commands 
    def find_files(self):
        """open native file finder to pass to add file list"""
        add_file_list = fd.askopenfilenames()
        self.parent.add_files(add_file_list)

    def remove_files(self):
        '''removes selected files from treeview'''
        for _file in self.file_list_view.selection():
            self.file_list_view.delete(_file)

        self.parent.update_file_list()

    def clear_files(self):
        '''clears all files from treeview'''
        for _file in self.file_list_view.get_children():
            self.file_list_view.delete(_file)

        self.parent.update_file_list()

class TreeviewFrame(ttk.Frame):
    def __init__(self, parent):
        self.treeview_frame = ttk.Frame.__init__(self, parent)
        self.parent = parent
        

        # just one column called 'filename'
        self.columns = ('Filename')
        self.make_file_list_view(self)



    def make_file_list_view(self, parent):
        ''' makes the file list view '''
        self.file_list_view = ttk.Treeview(
                                parent,
                                column=self.columns,
                                show='headings')


        # drag and drop
        self.file_list_view.drop_target_register(DND_FILES)
        self.file_list_view.dnd_bind('<<Drop>>',
            lambda dropped_files: self.drop_files(dropped_files))

        # the single column for filenames
        # TODO: horizontal scrollbar
        #  it is really annoying to get tkinter to change the horizontal
        #  scrollbar if you add files... now it is just some big number
        self.file_list_view.column('Filename',
                                anchor="w",
                                stretch=True,
                                width=10,
                                minwidth=1000
                                )

        self.file_list_view.heading(column='#1',
                                text='Filename',
                                anchor="w"
                                )

        
        self.file_list_view_y_scroll = ttk.Scrollbar(
                                parent,
                                orient='vertical',
                                command=self.file_list_view.yview
                                )
        self.file_list_view.configure(
                                yscrollcommand=self.file_list_view_y_scroll.set)

        self.file_list_view_x_scroll = ttk.Scrollbar(
                                parent,
                                orient='horizontal',
                                command=self.file_list_view.xview
                                )
        
        self.file_list_view.configure(
                                xscrollcommand=self.file_list_view_x_scroll.set)

        self.file_list_view_y_scroll.pack(side='right', fill='y')
        self.file_list_view_x_scroll.pack(side='bottom', fill='x', expand=False)
        self.file_list_view.pack(fill='both', side='left', expand=1)


    def drop_files(self, dropped_files: TkinterDnD.DnDEvent):
        """change file lists based on drag + dropped files"""
        dropped_files = self.file_list_view.tk.splitlist(dropped_files.data)
        self.parent.add_files(dropped_files)

    

class SourceFormatFrame(ttk.LabelFrame):
    ''' frame for the source format options
    args:
        parent: the parent frame (should be OptionsFrame)
        source_format_var: the variable saying what the source format
        for transliteration is
        target_format_frame: the frame with target format things
        (so as to communicate and make certain options invalid)
    '''
    def __init__(
        self,
        parent,
        options_interface):
        self.source_format_section_frame = ttk.LabelFrame.__init__(
            self,
            parent,
            text='Source format')
        self.parent = parent

        # make source format variable accessible to fns
        self.options_interface = options_interface
        self.source_format_var = options_interface.get('source_format_var')
        self.font_search_menu = options_interface.get('font_search_menu')
        self.chosen_font = options_interface.get('chosen_font')
        self.make_source_buttons(self)

    def make_source_buttons(self, parent):
        """makes the source format option buttons

        Arguments:
            parent -- parent frame
        """
        self.straight_source = ttk.Radiobutton(
                        parent,
                        text='Straight',
                        variable=self.source_format_var,
                        value=FileFormat.STRAIGHT,
                        command=self.parent.source_target_radio_update
                                )
        self.straight_source.state(['selected'])
        self.options_interface.update({'straight_source_radio' : self.straight_source})

        self.APA_source = ttk.Radiobutton(
                        parent,
                        text='APA phonetics Unicode',
                        variable=self.source_format_var,
                        value=FileFormat.APAUNICODE,
                        command=self.parent.source_target_radio_update
                        )
        self.options_interface.update({'APA_source_radio' : self.APA_source})

        self.orthog_source = ttk.Radiobutton(
                        parent,
                        text='Practical orthography',
                        variable=self.source_format_var,
                        value=FileFormat.ORTHOGRAPHY,
                        command=self.parent.source_target_radio_update
                        )
        self.options_interface.update({'orthog_source_radio' : self.orthog_source})
            
        ##### pack up source section
        self.straight_source.pack(side='top', anchor='nw')
        self.APA_source.pack(side='top', anchor='nw')
        self.orthog_source.pack(side='top', anchor='nw')


class TargetFormatFrame(ttk.LabelFrame):
    ''' frame for the target format options
    args:
        parent: the parent frame (should be OptionsFrame)
        target_format_var: the variable saying what the target format
        should be'''
    def __init__(
        self,
        parent,
        options_interface):
        self.target_format_section_frame = ttk.LabelFrame.__init__(
            self,
            parent,
            text='Target format')
        self.parent = parent

        # make the target format variable accesible to fns
        self.options_interface = options_interface
        self.source_format_var = options_interface.get('source_format_var')
        self.target_format_var = options_interface.get('target_format_var')
        self.make_target_buttons(self)

    def make_target_buttons(self, parent):
        """makes the source format option buttons

        Arguments:
            parent -- _description_
        """
        self.APA_target = ttk.Radiobutton(
                parent,
                text='APA phonetics Unicode',
                variable=self.target_format_var,
                value=FileFormat.APAUNICODE,
                command=self.parent.source_target_radio_update)
        self.options_interface.update({'APA_target_radio' : self.APA_target})

        self.orthog_target = ttk.Radiobutton(
                parent,
                text = 'Practical orthography',
                variable = self.target_format_var,
                value= FileFormat.ORTHOGRAPHY,
                command=self.parent.source_target_radio_update)
        self.orthog_target.state(['selected'])

        self.options_interface.update({'orthog_target_radio' : self.orthog_target})

        self.APA_target.pack(side='top', anchor='nw')
        self.orthog_target.pack(side='top', anchor='nw')


class DestinationFrame(tk.LabelFrame):
    """section where user chooses where target files go
    """
    def __init__(
        self,
        parent,
        options_interface):
        self.destination_frame = ttk.LabelFrame.__init__(
            self,
            parent,
            text='Save transliterated file...'
        )
        self.parent = parent
        self.options_interface = options_interface
        self.output_destination_is_elsewhere = options_interface.get('output_destination_is_elsewhere')
        self.output_path_var = options_interface.get('output_path_var')
        self.make_target_buttons(self)

    def make_target_buttons(self, parent):
        '''put together target destination (where transliterated files go)
        section'''

        # radio to say "file goes in same place"
        self.target_in_place_radio = ttk.Radiobutton(
                parent,
                text='In place',
                variable=self.output_destination_is_elsewhere,
                value=False,
                command = self.target_destination_is_elsewhere_update)
        self.target_in_place_radio.state(['selected'])

        # radio to say "file goes elsewhere"
        self.target_to_destination_radio = ttk.Radiobutton(
                parent,
                text = 'To destination...',
                variable= self.output_destination_is_elsewhere,
                value=True,
                command = self.target_destination_is_elsewhere_update)

        # entry place for destination path
        self.output_path_entry = ttk.Entry(
                parent,
                textvariable=self.output_path_var)
        
            # self.target_to_destination_path_entry.state(['disabled'])

        # button to browse for the file
        self.output_path_find_button = ttk.Button(
                parent,
                text='Browse...',
                command=self.find_output)
        self.output_path_find_button.state(['disabled'])

        self.target_in_place_radio.pack(side='top', fill='both')
        self.target_to_destination_radio.pack(side='top', fill='both')
        self.output_path_entry.pack(side='top', fill='both')
        self.output_path_find_button.pack(side='top', fill='both')


    def find_output(self):
        '''
        bring up file finder to see where output files should go
        '''

        outputdir = fd.askdirectory(initialdir= './')
        
        if outputdir == '':
            self.output_path_var.set('./')
        else:
            self.output_path_var.set(outputdir)

    ### functions follow

    def target_destination_is_elsewhere_update(self):
        """
        update radio button in target destination type
        
        """

        # if the setting basically set to "not in place"
        if self.output_destination_is_elsewhere.get() is True:
            self.output_path_entry.state(['!disabled'])
            self.output_path_find_button.state(['!disabled'])

        # if the setting is set to "in place"
        if self.output_destination_is_elsewhere.get() is False:
            self.output_path_entry.state(['disabled'])
            self.output_path_find_button.state(['disabled'])

class FontSearchFrame(ttk.Frame):
    """ section where user chooses which font to search by
    which I really should deprecate, because it is not good---
    it is just a holdout from the old days of the Word macro"""

    def __init__(self, parent):
        
        self.font_search_frame = ttk.Frame.__init__(self, parent)

        self.parent = parent
        self.font_options_straight = ['Straight']
        self.font_options_extended = [
            'Straight',
            'BC Sans',
            'Times New Roman',
            'Times',
            'Arial',
            'Tahoma',
            ]

        
        self.chosen_font = parent.chosen_font
        self.font_options = self.font_options_straight
        self.make_font_search_menu(self)

    def make_font_search_menu(self, parent):
        """make the menu
        """

        self.font_search_menu = ttk.OptionMenu(
            parent,
            self.chosen_font,
            *self.font_options)
        
        self.font_search_menu.state(['disabled'])
        self.font_search_menu.pack(fill='x')
        
        

    def font_update(self):
        '''updates font list based on some circumstances
        (whether source format is Straight, etc.)

        ADD "Other" later 

        even better... add not doing this by stupid font
        '''

        self.font_search_menu["menu"].delete(0, "end")

        source_format_var = self.parent.source_format_var.get()

        if source_format_var == FileFormat.STRAIGHT:
            self.font_search_menu.state(['disabled'])
            self.chosen_font.set("Straight")
            pass

        else:
            self.font_search_menu.state(['!disabled'])
            for i in self.font_options_extended:
                self.font_search_menu["menu"].add_command(
                    label=i,
                    command=lambda value=i:
                        self.chosen_font.set(value))
    # TODO
    # if self.font_search_var.get() == 'Other...'

class WordlistSearchFrame(ttk.Frame):
    """frame for options related to wordlist search"""

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text='Wordlist search')

        self.parent = parent

        self.search_method_var = parent.search_method_var

    

class SearchMethodFrame(ttk.LabelFrame):
    """the frame where the user chooses whether to search with font
    (bad) or by wordlist (good)

    """

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text='Search method')


        self.source_format_var = parent.source_format_var
        self.search_method_var = parent.search_method_var
        self.chosen_font = parent.chosen_font
        
        self.font_search_frame = FontSearchFrame(self)
        self.wordlist_search_frame = WordlistSearchFrame(self)
        
        self.font_update = self.font_search_frame.font_update
        self.make_search_method_buttons(self)

        self.wordlist_search_frame.pack(side='top')

    def make_search_method_buttons(self, parent):
        """makes the buttons to choose the search method
        """
        self.search_method_wordlist_radio = ttk.Radiobutton(
            parent,
            text='Wordlist search',
            variable=self.search_method_var,
            value='Wordlist',
            command=self.switch_search_method)
        self.search_method_wordlist_radio.state(['selected'])


        self.search_method_font_radio = ttk.Radiobutton(
            parent,
            text='Font search',
            variable=self.search_method_var,
            value='Font',
            command=self.switch_search_method)
        self.search_method_wordlist_radio.pack(fill='x')
        self.search_method_font_radio.pack(fill='x')


    def switch_search_method(self):
        """switches the search method frame from wordlist to
        font search
        """

        match self.search_method_var.get():
            case 'Wordlist':
                self.font_search_frame.pack_forget()
                self.wordlist_search_frame.pack(side='top', fill='x')
            case 'Font':
                self.wordlist_search_frame.pack_forget()
                self.font_search_frame.pack(side='top', fill='x')




class OptionsSection(ttk.Frame):
    ''' section where user chooses options:
    source format: Straight, orthography, or APA Unicode
    target format: Orthography or APA Unicode
    target destination: where transliterated files go--
        somewhere else or same place
    font search: which font to search by for what to transliterate'''

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        
        # initialize variables

        # list of files to transliterate
        self.source_file_list = parent.source_file_list

        # format of source file
        self.source_format_var = tk.StringVar()
        self.source_format_var.set(FileFormat.STRAIGHT)

        # format of target file
        self.target_format_var = tk.StringVar()
        self.target_format_var.set(FileFormat.ORTHOGRAPHY)

        # what kind of target (dir, all files in place)
        self.output_destination_is_elsewhere = tk.BooleanVar()
        self.output_destination_is_elsewhere.set(False)

        # list of fonts
        # (not needed?)

        

        # font to search by
        self.chosen_font = tk.StringVar()
        self.chosen_font.set('Straight')

        # where the target should go (if changed)
        self.output_path_var = tk.StringVar()
        self.output_path_var.set(None)    

        self.search_method_var =  tk.StringVar()
        self.search_method_var.set('Wordlist')

        self.options_interface = {
            'source_format_var' : self.source_format_var,
            'target_format_var' : self.target_format_var,
            'chosen_font'  : self.chosen_font,
            'search_method_var': self.search_method_var,
            'output_destination_is_elsewhere' : self.output_destination_is_elsewhere,
            'output_path_var' : self.output_path_var
            }

        #! is it better to leave options_interface as a parameter
        #! or have it accessible as a parent attribute?
        # accessible it as a parent attribute i am so stupid
        self.source_format_frame = SourceFormatFrame(self, self.options_interface)
        self.target_format_frame = TargetFormatFrame(self, self.options_interface)
        self.search_method_frame = SearchMethodFrame(self)
        self.destination_frame = DestinationFrame(self, self.options_interface)
        
        self.transliterate_files_frame = TransliterateFilesFrame(self, self.options_interface)

        self.source_format_frame.pack(side='top', fill='both', pady=10)
        self.target_format_frame.pack(side='top', fill='both', pady=10)
        self.search_method_frame.pack(side='top', fill='x', pady=10)
        self.destination_frame.pack(side='top', fill='both', pady=10)
        self.transliterate_files_frame.pack(side='top', fill='x', pady=10)

        self.font_update = self.search_method_frame.font_update

    def source_target_radio_update(self):
        """updates all the radio buttons based on chosen options,
        especially to disable radio buttons based on source format
        """

        self.search_method_frame.font_update()

        source_format_var = self.options_interface.get('source_format_var') # type: tk.StringVar
        target_format_var = self.options_interface.get('target_format_var') # type: tk.StringVar
        APA_target_radio = self.options_interface.get('APA_target_radio') # type: ttk.Radiobutton
        orthog_target_radio = self.options_interface.get('orthog_target_radio') # type: ttk.Radiobutton

        source_format = FileFormat.from_string(source_format_var.get())
        target_format = FileFormat.from_string(target_format_var.get())


        match source_format:
            case FileFormat.APAUNICODE:
                APA_target_radio.configure(state=['disabled'])
                orthog_target_radio.configure(state=['!disabled'])
                target_format_var.set(FileFormat.ORTHOGRAPHY)
            case FileFormat.ORTHOGRAPHY:
                orthog_target_radio.configure(state=['disabled'])
                APA_target_radio.configure(state=['!disabled'])
                target_format_var.set(FileFormat.APAUNICODE)
            case FileFormat.STRAIGHT:
                APA_target_radio.configure(state=['!disabled'])
                orthog_target_radio.configure(state=['!disabled'])        

class TransliterateFilesFrame(ttk.Frame):
    """mostly just a place for one button

    """
    
    def __init__(self, parent, options_interface):
        self.transliterate_files_frame = ttk.Frame.__init__(self, parent)

        self.parent = parent
        
        # get all the stupid variables
        self.source_file_list = parent.source_file_list
        self.source_format_var = parent.source_format_var
        self.target_format_var = parent.target_format_var
        self.output_destination_is_elsewhere = parent.output_destination_is_elsewhere
        self.search_method_var = parent.search_method_var
        self.chosen_font = parent.chosen_font
        
        self.transliterate_button_init(self)

    def transliterate_button_init(self, parent):
        '''transliterate that sucker!!!!!!!!'''

        self.transliterate_button = ttk.Button(
            parent,
            text = "Transliterate",
            command = self.transliterate_files
        )
        
        self.transliterate_button.pack(side='bottom', fill='both')


    def transliterate_files(self):
        '''run transliterator on files
        '''
        
        source_format = FileFormat.from_string(self.source_format_var.get())
        target_format = FileFormat.from_string(self.target_format_var.get())
        output_dir = self.parent.output_path_var.get()
        output_dest_elsewhere = self.output_destination_is_elsewhere.get()
        search_method_var = self.parent.search_method_var.get()
        chosen_font = self.parent.chosen_font.get()

        docx_transliterands = {
            TransliterandFile(
                Path(file),
                source_format,
                target_format)
            for file in filter(
                lambda x: Path(x).suffix == '.docx',
                self.source_file_list
                )
            }

        txt_transliterands = {
            TransliterandFile(
                Path(file),
                source_format,
                target_format)
            for file in filter(
                lambda x: Path(x).suffix == '.txt',
                self.source_file_list
                )
            }



        if output_dest_elsewhere is True:
            for file in docx_transliterands | txt_transliterands:
                file.update_target_path(output_dir)

        transliterands = {'docx' : docx_transliterands,
                          'txt' : txt_transliterands}


        if search_method_var == 'Wordlist':
            tr.FileController(transliterands)
            # tr.file_processor(
            #         transliterands,
            #         search_method='Wordlist')

        if search_method_var == 'Font':
            tr.file_processor(
                    transliterands,
                    search_method='Font',
                    font=chosen_font)

    

class FileTransliterator(ttk.Frame):
    '''
    page with all the main file transliterator stuff
    '''
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(
                    self,
                    parent,
                    *args,
                    **kwargs)
        self.parent = parent
        
        self.source_file_list = set()

        self.source_file_section = SourceFileFrame(self)
        self.options_section = OptionsSection(self)

        # pack the two halves up
        self.source_file_section.pack(side='left', fill='both', expand='2')
        self.options_section.pack(side='right', fill='both', padx=10, pady=10)




class InstantSourceFrame(ttk.LabelFrame):
    """the frame that holds the source text box for the
    instant transliterator

    
    """
    def __init__(self, parent):
        self.instant_source_frame = ttk.LabelFrame.__init__(
            self,
            parent,
            text='Source format'
        )

        self.parent = parent
        self.make_instant_source_radio_buttons(self)
        self.make_instant_source_textbox(self)


    def make_instant_source_radio_buttons(self, _parent):
        """make the buttons for choosing which format the source text is in

        """
        self.instant_source_button_frame = ttk.Frame(_parent)
        self.instant_straight_source = ttk.Radiobutton(
                            self.instant_source_button_frame,
                            text='Straight',
                            variable=self.parent.instant_source_format_var,
                            value=FileFormat.STRAIGHT,
                                    )
        self.instant_straight_source.state(['selected'])

        self.instant_APA_source = ttk.Radiobutton(
                            self.instant_source_button_frame,
                            text='APA phonetics Unicode',
                            variable=self.parent.instant_source_format_var,
                            value=FileFormat.APAUNICODE,
                            )

        self.instant_orthog_source = ttk.Radiobutton(
                            self.instant_source_button_frame,
                            text='Practical orthography',
                            variable=self.parent.instant_source_format_var,
                            value=FileFormat.ORTHOGRAPHY,
                            )
        
        ##### pack up source button section
        self.instant_straight_source.pack(side='left', anchor='nw', padx=4, pady=4)
        self.instant_APA_source.pack(side='left', anchor='nw', padx=4, pady= 4)
        self.instant_orthog_source.pack(side='left', anchor='nw', padx=4, pady=4)

        self.instant_source_button_frame.pack(side='top', anchor='nw')

    
    def make_instant_source_textbox(self, parent):
        '''
        give the text box for the source text
        '''
        self.source_text = ScrolledText(parent)
        self.source_text.pack(side='top', fill='both', expand=3)

class InstantTargetFrame(ttk.LabelFrame):
    """frame containing the text box where the transliterated text goes
    """
    def __init__(self, parent):
        self.instant_target_frame = ttk.LabelFrame.__init__(
            self,
            parent,
            text='Target format'
        )
    
        self.parent = parent
        self.make_instant_target_radio_buttons(self)
        self.transliterated_scrolledtext_init(self)


    def make_instant_target_radio_buttons(self, parent):
        """make the buttons for choosing the output format"""

        self.instant_target_button_frame = ttk.Frame(parent)

        self.instant_APA_target = ttk.Radiobutton(
                            self.instant_target_button_frame,
                            text='APA phonetics Unicode',
                            variable=self.parent.instant_target_format_var,
                            value=FileFormat.APAUNICODE,
                            )

        self.instant_orthog_target = ttk.Radiobutton(
                            self.instant_target_button_frame,
                            text='Practical orthography',
                            variable=self.parent.instant_target_format_var,
                            value=FileFormat.ORTHOGRAPHY,
                            )

        self.instant_APA_target.pack(
                            side='left',
                            anchor='sw',
                            padx=4,
                            pady=4)
        self.instant_orthog_target.pack(side='left', anchor='sw', padx=4,pady=4)

        self.instant_target_button_frame.pack(side='top', anchor='w', pady=4)

    def transliterated_scrolledtext_init(self, parent):
        '''
        give the text box for the source text
        '''
        self.target_text = ScrolledText(parent)
        self.target_text.pack(side='top', fill='both', expand=2)

class InstantTransliterator(ttk.Frame):
    '''
    transliterates text instantly
    
    needs cleaned up since i just copied a bunch of stuff over
    '''
    def __init__(self, parent, *args, **kwargs):
        self.instant_transliterator_holder = ttk.Frame.__init__(
            self,
            parent,
            padding="3 3 12 12")
        
        self.parent = parent

        self.instant_source_format_var = tk.StringVar()
        self.instant_source_format_var.set(FileFormat.STRAIGHT)
        self.instant_target_format_var = tk.StringVar()
        self.instant_target_format_var.set(FileFormat.ORTHOGRAPHY)

        self.instant_source_frame = InstantSourceFrame(self)
        self.instant_target_frame = InstantTargetFrame(self)

        self.instant_source_frame.pack(side='top', fill='both', expand=2)
        self.instant_target_frame.pack(side='top', fill='both', expand=1)

        self.make_instant_transliterate_button(self)

        self.instant_source_frame.pack(side='top')
        self.instant_target_frame.pack(side='top')
        self.instant_transliterate_button.pack(side='top', anchor='w')

    def make_instant_transliterate_button(self, parent):
        '''
        instantly transliterates !
        '''
        
        self.instant_transliterate_button = ttk.Button(
            parent,
            text = "Transliterate",
            command = self.instant_transliterate_text
        )
        self.instant_transliterate_button.pack(side='top')

    def instant_transliterate_text(self):
        '''
        transliterates the text in the source box and puts it
        in the transliterated box
        '''

        self.source_text = self.instant_source_frame.source_text.get('1.0','end-1c')
        source_format = FileFormat.from_string(self.instant_source_format_var.get())
        target_format = FileFormat.from_string(self.instant_target_format_var.get())

        transliterated_text = tr.string_processor(
            self.source_text,
            source_format,
            target_format)
        
        
        self.instant_target_frame.target_text.delete('1.0', 'end-1c')
        self.instant_target_frame.target_text.insert('end-1c', transliterated_text)

class MainApplication(ttk.Notebook):
    def __init__(self, parent, *args, **kwargs):
            self.parent = parent
            ttk.Notebook.__init__(self, parent, padding="3 3 12 12",style='noborder.TNotebook')
        
            
            file_transliterator_frame = FileTransliterator(self)
            instant_transliterator_frame = InstantTransliterator(self)

            file_transliterator_frame.pack(fill='both')
            instant_transliterator_frame.pack(fill='both', expand=True)

            self.add(file_transliterator_frame, text='File Transliterator')
            self.add(instant_transliterator_frame, text='Instant transliterator')

            self.pack(fill='both')

def make_app():
    ''' just makes the dang app '''
    root = TkinterDnD.Tk()
    root.title('Hul’q’umi’num’ Transliterator v0.4')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    make_app()
