# XtremeUpdater
*Note: XtremeUpdater is in alpha and is not stable at all. Dll backing and restoring should work, but please backup your dlls manually before using XtremeUpdater.*

Website is located at https://xtremeware.github.io/XtremeUpdater.
Support and chat at [discord](https://discord.gg/ZD6rxw9).

## v0.52
*Code cleanup*

**Bugfixes**
 - Fixed bug causing freeze when selecting directory without any dlls.
 - Fixed bug which caused refresh button to crash the app

## v0.51
*Note: Added support for kivy 1.10.1*

 **New features**
  - You can now start games from the game collection
  
  *Note: Some Steam games may not start correctly due to missing initialization of the Steam Client.*

## v0.5
*Note: We are removing `source.py` and all of it's deps in this update and everything is now ported to [kivy](https://github.com/kivy/kivy) gui.*

  **New features**
   - Mouse highlight
   - *Game Collection*

  **Removed features**
   - Available dlls cache

  **Tweaks**
   - Made few tweaks to buttons
   - Added texture to the head
   - App title is now bold
   - Changed app title colors
   - Path input font is now bold

  **Bugfixes**
   - Fixed bug which caused *dll list* to not display during 2nd or more directory selection
   - Fixed bug which caused *select all* button to stay enabled after updating completion
   - Fixed bug which caused to load available dlls twice

## v0.4
**Tweaks**
   - Dlls now do not backup and overwrite when they are not of a newer version

**Bugfixes**
   - Fixed error when updating dlls in some cases

## v0.3
  **New features**
   - *Select all* button to the *dll view*
   - *Restore* support
   - *Tweaks*
   - *Refresh* button in case sync fails

   **Tweaks**
   - Tweaked *Update* and *Restore* buttons' behavior
   - Changed scrollbar color so it's now visible when scrolling over selected dlls
   - Moved *info* text a bit up
   - Redesigned texture for navigation buttons; depth
   - Increased window size from *800x450* to *1000x550*

  **New system tweaks**
   - Delete tempdir

   **Bugfixes**
   - *Update* and *Restore* buttons are no longer visible when updating dlls

## v0.2
 **New features**
  - Added dll updater

## v0.1
**Bugfixes**
- Fixed syncing error loop when syncing with GitHub
- When sync error is raised, _Games_ tab will now reset to its default state after 2 seconds