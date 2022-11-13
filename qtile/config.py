import subprocess
import os
from libqtile import bar, layout, widget, hook, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"
terminal = 'kitty'
BGimg= '~/.config/qtile/wallpaper3.png'

@hook.subscribe.startup_once
def startup():
    home = os.path.expanduser('~/.config/qtile/startup.sh')
    subprocess.Popen([home])

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    # Toggle between split and unsplit sides of stack.
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"],"Return",lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(terminal)),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawn("rofi -show drun")),
   
    # Media

    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    
    # Brightness 
    
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")), 
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Screenshot
    Key([mod, "shift"], "s", lazy.spawn("scrot -e 'xclip -selection clipboard -t image/png -i $f'")), 
]
# Key([mod, "shift"], "s", lazy.spawn("scrot -s -f '/home/jeanne/Screenshots/%b%d::%H%M%S.png'")), 

groups = [Group(i) for i in ["", "", "", "", ""]]

for i, group in enumerate(groups):
    actual_key=str(i + 1)
    keys.extend([
            # Move to a Workspace
            Key([mod], actual_key, lazy.group[group.name].toscreen()),

            # Move windows to a workspace
            Key([mod, "shift"], actual_key, lazy.window.togroup(group.name)),
        ])

layouts = [
    layout.Columns(
        border_focus='#3C8ECD',
        border_normal='#102B3F',
        border_width=4,
        margin=5,
        margin_on_single=5,
        ),
    layout.Max(
        border_focus='#3C8ECD',
        border_normal='102B3F',
        border_width=4,
        margin=5,
    ),
]

widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        
        wallpaper=BGimg,
        wallpaper_mode='fill',

        top=bar.Bar(
                [    
                widget.GroupBox(
                    active='#000000', inactive='#e5e5e5', background='#FFFFFF',
                    highlight_method='line', highlight_color='#FFFFFF',
                    urgent_border='#FF0000', this_current_screen_border='#232b2b',
                    ),

                widget.Spacer(),
                
                widget.Clock(
                    format="%Y-%m-%d %a %H:%M",
                    background='#FFFFFF', foreground='#000000',
                    mouse_callbacks={'Button1':lazy.spawn("khal calendar")},
                    ),
        
                widget.Spacer(),

                widget.Systray(),
                widget.Battery(
                    charge_char='C', discharge_char='D',
                    format=" {char} {percent:2.0%} {hour:d}:{min:02d}",
                    low_background='#E63946', low_foreground='#FFFFFF', low_percentage=0.21,
                    update_interval=10, 
                    background='#FFFFFF', foreground='#000000',
                    ),
                widget.ThermalSensor(
                    format=' {temp:.1f}{unit}',
                    background='#FFFFFF', foreground='#000000',
                    #background_alert='#E63946', foreground_alert='#FFFFFF',
                    #threshold=40,
                    ),
                widget.Wlan(
                    format=' {essid} {percent:2.0%}',
                    disconnected_message='Desconectado',
                    background='#FFFFFF', foreground='#000000',
                    mouse_callbacks={'Button1':lazy.spawn("iwgtk")},
                    ),
                widget.Volume(
                    fmt=': {}',
                    mouse_callbacks={'Button1':lazy.spawn("pavucontrol")},
                    background='#FFFFFF', foreground='#000000',
                    ),
                ],
            30,
            background='#00000000',
            border_width=[5, 5, 0, 5], #Arriba, Derecha, Abajo, Izquierda
            border_color='#00000000',
        ),
    ),
]
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# Run the utility of `xprop` to see the wm class and name of an X client.
layout.Floating.default_float_rules,
Match(wm_class="confirmreset"),  # gitk
Match(wm_class="makebranch"),  # gitk
Match(wm_class="maketag"),  # gitk
Match(wm_class="ssh-askpass"),  # ssh-askpass
Match(title="branchdialog"),  # gitk
Match(title="pinentry"),  # GPG key password entry

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

