To Install: Copy the RendLauncher.ini, dll-injection.exe, RendLauncher.exe and UniversalUE4Unlocker.dll to your Rend Game folder(You'll see Rend.exe and RendClient.exe).

Run RendLauncher.exe as Admin if you require the UUE4U fix (it needs be run Admin to use Add/Remove the firewall block/unblock function)

If your Game still closes you may need to set the Firewall Unblock delay to something higher, 15 seemed to work for me may need to be higher if running the game from a HDD.

Edit the RendLauncher.ini and enter in your own details (If you don't have it launching RendLauncher.exe will generate one)

[Settings] \
name = NAME \
faction = 1,2,3 \
ipport = URL/IP:PORT \
delay = 15 


The injector used is from https://github.com/craig-rylance/dll-injector.

The DLL file was from UUE4U (google it).

You may get a error complaining about a Temp folder, I can't figure it out and it doesn't stop the program from working. \
New to githubs workings but I think other people can contribute? feel free to fix it. \
Would like to make it so the user input fields write to the ini file may fix that in the future.


The PyCode was from Grok.


GG's
