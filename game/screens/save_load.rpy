## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load


## The width and height of thumbnails used by the save slots.
define config.thumbnail_width = 400
define config.thumbnail_height = 400 / 16 * 9
define gui.file_slot_cols = 1
define gui.file_slot_rows = 4
define slot_verticle_spacing = 40
define text_length = 20
define slot_x_size = 600
define slot_y_size = 160


screen save():

    tag menu

    # add HBox(Transform("#292835", xsize=350), "#21212db2") # The background; can be whatever

    use file_slots(_("Save"))


screen load():

    tag menu

    # add HBox(Transform("#292835", xsize=350), "#21212db2") # The background; can be whatever

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(
        pattern=_("Page {}"), auto=_("Automatic saves"),
        quick=_("Quick saves"))

    use game_menu(title)

    fixed:
        xalign 0.5 
        yalign 0.5
        ## This ensures the input will get the enter event before any of the
        ## buttons do.
        order_reverse True

        ## The page name, which can be edited by clicking on it.
        ## This can be pretty easily removed if you want.
        ## Don't forget to also remove the `default` at the top if so.

        side "c":
            area (350, 180, 2000, 2000)
            viewport id "slot":
                grid gui.file_slot_cols gui.file_slot_rows:
                    xalign 0.5 yalign 0.0 spacing slot_verticle_spacing
                    for i in range(gui.file_slot_rows):
                        grid 2 1:
                            style_prefix "slot"
                            spacing 50

                            python:
                                def get_only_characters(string):
                                    flag = 0
                                    res = ""
                                    for i in range(len(string)):
                                        curr_char = string[i]
                                        if curr_char == "{":
                                            flag = 1
                                        elif curr_char == "}":
                                            flag = 0
                                        elif flag == 0:
                                            res += curr_char
                                    return res
                                slot = i * 2 + 1
                                name_to_save = ""
                                strip = lambda string : string \
                                    if len(string) <= text_length \
                                    else string[: text_length] + "……"

                                if len(_history_list) != 0:
                                    if type(_history_list[-1].who) is NoneType:
                                        name_to_save = f"Chapter {chap_index} \n" + strip(get_only_characters(_history_list[-1].what))
                                    else: 
                                        name_to_save = (
                                            f"Chapter {chap_index} \n"
                                            "【" + get_only_characters(_history_list[-1].who) + "】 "
                                            + strip(get_only_characters(_history_list[-1].what))
                                        )
                                current_chapter = f"Chapter {chap_index}"
                            
                            button:
                                action [
                                    SetVariable("save_name", name_to_save),
                                    FileAction(slot)
                                ]

                                hbox:
                                    spacing 10
                                    if FileTime(slot):
                                        add FileScreenshot(slot) align(0.1, 0.1) zoom 0.6
                                        vbox:
                                            spacing 10
                                            text FileTime(slot, format=_("{#file_time}%Y/%m/%d %H:%M")):
                                                style "slot_time_text"
                                            
                                            # text current_chapter:
                                            #     style "slot_name_text"

                                            text FileSaveName(slot):
                                                style "slot_button_text"
                                    else:
                                        image "gui/button/gray_image.png" zoom 0.6
                                        vbox:
                                            text "尚无记录":
                                                style "no_record_slot_button_text"
                            
                            python:
                                def get_only_characters(string):
                                    flag = 0
                                    res = ""
                                    for i in range(len(string)):
                                        curr_char = string[i]
                                        if curr_char == "{":
                                            flag = 1
                                        elif curr_char == "}":
                                            flag = 0
                                        elif flag == 0:
                                            res += curr_char
                                    return res
                                slot = slot + 1
                                name_to_save = ""
                                strip = lambda string : string \
                                    if len(string) <= text_length \
                                    else string[: text_length] + "……"

                                if len(_history_list) != 0:
                                    if type(_history_list[-1].who) is NoneType:
                                        name_to_save = f"Chapter {chap_index} \n" + strip(get_only_characters(_history_list[-1].what))
                                    else: 
                                        name_to_save = (
                                            f"Chapter {chap_index} \n"
                                            "【" + get_only_characters(_history_list[-1].who) + "】 "
                                            + strip(get_only_characters(_history_list[-1].what))
                                        )
                                current_chapter = f"Chapter {chap_index}"
                                        
                            button:
                                action [
                                    SetVariable("save_name", name_to_save),
                                    FileAction(slot)
                                ]

                                hbox:
                                    spacing 10
                                    if FileTime(slot):
                                        add FileScreenshot(slot) align(0.1, 0.1) zoom 0.6
                                        vbox:
                                            spacing 10
                                            text FileTime(slot, format=_("{#file_time}%Y/%m/%d %H:%M")):
                                                style "slot_time_text"
                                            
                                            # text current_chapter:
                                            #     style "slot_name_text"
                                            
                                            text FileSaveName(slot):
                                                style "slot_button_text"
                                    else:
                                        image "gui/button/gray_image.png" zoom 0.6
                                        vbox:
                                            text "尚无记录":
                                                style "no_record_slot_button_text"

                                key "save_delete" action FileDelete(slot) 

        ## Buttons to access other pages.
        vbox:
            style_prefix "page"
            hbox:
                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()

            # if config.has_sync:
            #     if CurrentScreenName() == "save":
            #         textbutton _("Upload Sync"):
            #             action UploadSync()
            #     else:
            #         textbutton _("Download Sync"):
            #             action DownloadSync()


style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color '#ff8335'

style slot_grid:
    xalign 0.5
    yalign 0.5
    spacing 15

style slot_time_text:
    size 21
    xalign 0.0
    color gui.dark_grey

style slot_name_text:
    size 21
    xalign 0.0
    color gui.dark_grey

style slot_vbox:
    spacing 12

style slot_button:
    xysize (slot_x_size, slot_y_size)
    padding (15, 15, 15, 15)
    background "gui/button/slot_idle.jpg"
    hover_background "gui/button/slot_hover.jpg"

style slot_button_text:
    size 21
    xalign 0.0
    idle_color gui.dark_grey
    hover_color gui.light_blue
    selected_idle_color gui.dark_grey
    font gui.text_font

style no_record_slot_button_text:
    size 21
    xalign 0.0
    idle_color gui.dark_grey
    hover_color gui.light_blue
    selected_idle_color gui.dark_grey

style page_hbox:
    xalign 0.5
    spacing 5

style page_vbox:
    xalign 0.5
    yalign 1.0
    spacing 5

style page_button:
    padding (15, 6, 15, 6)
    xalign 0.5

style page_button_text:
    color gui.dark_grey
    hover_color gui.light_grey
    selected_color "#fff"
    font "fonts/Aboreto-Regular.ttf"

