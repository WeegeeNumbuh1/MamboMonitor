#!/bin/bash
# Install script for MamboMonitor
# Repurposed from my other project, FlightGazer
# Last edited: v.0.2.0
# by: WeegeeNumbuh1
export DEBIAN_FRONTEND="noninteractive"
STARTTIME=$(date '+%s')
STARTMONOTONIC=$(cat /proc/uptime | awk '{print $1}')
BASEDIR=$(cd `dirname -- $0` && pwd)
export PYTHONUNBUFFERED=1
export PIP_ROOT_USER_ACTION=ignore
VENVPATH=/opt/MamboMonitor
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
FADE='\033[2m'
WHITEHIGH='\033[0;30;47m'

if [ `id -u` -ne 0 ]; then
	>&2 echo -e "${RED}>>> ERROR: This script must be run as root.${NC}"
	sleep 1s
	exit 1
fi
if ! command -v apt >/dev/null 2>&1; then
	echo -e "${NC}${RED}>>> ERROR: Setup cannot continue. This system does not use apt.${NC}"
	sleep 2s
	exit 1
fi

servicefile_heredoc() {
	cat <<- EOF > /etc/systemd/system/mambomonitor.service
	[Unit]
	Description=Umamusume gif player for rgbmatrix displays
	After=multi-user.target
	Documentation="https://github.com/WeegeeNumbuh1/MamboMonitor"

	[Service]
	User=root
	ExecStartPre=/bin/bash "${BASEDIR}/tools/splash_screen_manager.sh"
	ExecStart=/usr/bin/python3 "${BASEDIR}/MatikanetannhauserMain.py" "${BASEDIR}/img_src"
	Type=simple
	OOMScoreAdjust=-500
	Nice=-8
	IOSchedulingClass=best-effort
	IOSchedulingPriority=0
	Restart=on-abnormal
	RestartSec=5s

	[Install]
	WantedBy=multi-user.target
	Also=mambo-bootsplash.service
	EOF
}

bootsplashservice_heredoc () {
	cat <<- EOF > /etc/systemd/system/mambo-bootsplash.service
	[Unit]
	Description=Matikanetannhauser boot splash screen
	DefaultDependencies=no
	After=local-fs.target
	Before=network.target
	RefuseManualStart=true
	Documentation="https://github.com/WeegeeNumbuh1/MamboMonitor"

	[Service]
	User=root
	ExecStart=/usr/bin/python3 "${BASEDIR}/tools/splash-sysinit.py"
	Type=simple
	Restart=no

	[Install]
	# start real early
	WantedBy=sysinit.target
	EOF
}

echo -ne "\033]0;MamboMonitor Installer\007" # set window title
echo -e "\n${ORANGE}>>> Welcome to MamboMonitor!${NC}"
sleep 2s
echo "Note: this just installs the service and"
echo "required Python packages so that"
echo "the main script runs at boot."
sleep 2s
echo "If you need to install the rgbmatrix library,"
echo "please use the 'rgbmatrix_install.sh' script"
echo "in the 'tools' directory."
sleep 5s

echo -e "\n${GREEN}>>> Installing Python packages...${NC}"
# no venv or requirements.txt? (skill issue)
# using a venv will come later (maybe)
apt-get install pip python3-requests -y
pip3 install --upgrade pydispatcher --break-system-packages
pip3 install --upgrade ruamel.yaml --break-system-packages
pip3 install --upgrade beautifulsoup4 --break-system-packages
pip3 install --upgrade fake-useragent --break-system-packages
pip3 install --upgrade RGBMatrixEmulator --break-system-packages

echo -e "\n${GREEN}>>> Installing system services...${NC}"
servicefile_heredoc
bootsplashservice_heredoc
systemctl daemon-reload
systemctl enable mambomonitor.service
systemctl enable mambo-bootsplash.service
systemctl status mambomonitor.service --no-pager
echo -e "\n${GREEN}>>> Install complete.${NC}"
sleep 2s
echo "Note: if you want to disable the automatic startup,"
echo "use the command 'systemctl disable mambomonitor'"
sleep 2s

echo -e "\n${WHITEHIGH}"
echo "    ::                                            ;TT,      ";
echo "   ;ttf;                                         .l;;l,     ";
echo "   !jrrr!                                        TTIilI     ";
echo "   Txxrxxri              ,lFxuvvuxFI           :Fliiilti    ";
echo ".cCcrxxnnuuvT.      :!uXYYYYXvuvczzvvt        ;tlIiiiI!!,   ";
echo ":ccrjrxnnnxvvvj,luzYYXXcXYYYXzzzzcvuuxi     ,llIIiiiiiI!i   ";
echo " lFTrxnnnnnnuzYXzcvzYXXXXXXzzcccvuunxxl    :iiiiiiiiiIIiI   ";
echo " IttrnxxnnYYXcYYYXzczXzzccvuuuuvvuuxjFF   .iiiiiIIIiiiIIl.  ";
echo "   TvnuXUzvzYdkkkdwJzcvvuuuuuunjffjfnnr,  ,IiiIIIIIIiiiI!.  ";
echo "   tcYYvXzcvLbbbkkbQvuuuunrFnJqbhhJ!frxrnn!iiiiiIIIIIiiii   ";
echo "   :YYXzzvuYpdbbbdQnxxjfxJpkaoooookxxnnnxFnvF;;iiIiIIIiI:   ";
echo "  .zCcunnnuucULLmwQnxXQdkaoooMMMoaCxnxxxnurjvvFi;iiIIIII    ";
echo "  JJcunnnnnnnxjfFJpbkhhaooMMMoohmjjrxnxnnnunfFvvT;IIiIi     ";
echo "  FXzvunnxFfjuJwdkhhaaaooooohpJFrxuuuuvvvuuunrTrvx!iI:      ";
echo "   jXvnrtjYwpdkkhhaaaoooakpwqqjxnuuuuuvcvvvvuunjtnvx:       ";
echo "   :luFrwkkhhhhaaaooakpmmpbkdvnnnxuvcvuvvcuvnnvux!Tnv,      ";
echo "    ,lLaaaaaaaaahbLcFTYdkkhdcvvcvvvccccccvuxxvvunr!TrF      ";
echo "     idaooooabwn!tfjxqkkhhqcvccczcvcvczccvuunnuxunx!fnt     ";
echo "   tnjuCwCzxFTfFrxnJbkkhkCvvvcccccvzmwzvvvvunnnxxnuxlTni    ";
echo " ;cvuTirrjnxxxxncmkkkhhpcuuvuxvvcYqdqkbQuvvvunrjjunnF.Tv!   ";
echo ":vcF..updqmmddbkhhhhkwunuucYcvcQpbbkkkbbqznrrjfjjjrnnI.tnT  ";
echo "vuT  jnFcwbkhhhhhkwYxjTirCXXCqdbkkkdXT;::;lITFjFjxxxxj  tu! ";
echo "nx! jXnrxvnxjTt::Tn..,:LULdbbkkkkbbCJqu;:,,,::Fjrxxxrj, .ju:";
echo ",jFjnuurxvunx:.Tqdm,,,,,Xpbbbkkkkkbbbhkm:,,.i;,Trrrjjjtl!Tn!";
echo "  IXJXvrxzvun:lt,;iIIi;,;kbkkkkkkkkC;rfii;:,;F;fxxrrrjj!iTr;";
echo "  .YUJcunzccu:FFcczzzzXcfkbbkkkkkkkJrcczXXzzuXIFxrrjjjjf.   ";
echo "  .XJYcvcXYzuczJTczXXXXcvbbkkkkkbkbLxXXzXzzzjJ!jjjjjjjjj;   ";
echo "   xYXvvczzvuvpbQfzXXXnFbkkkkkkkkkbkUrXXXXctQpnjrFjjjjrF:   ";
echo "   ,uzvuvcvunnXwdpwmLqbbbbbbbbbbbbbbkbwLUJmppQcjFjrrrrrj    ";
echo "    ;!jxnvnnnnxvQLwmqmwddXcvccuuuuvqddwmwQmJYnrFjFjjrrj,    ";
echo "   .IrnnrxxnxxnxXCCmLqqpwvwmmmmmQQmvpqpLwCLYnjFFfffFF!      ";
echo "   ilIIIFxnxxxxjFcJLmmmmwCzLmmmmmUvwwwwQLJzFFFfTffffT.      ";
echo "  :!!lI::jxxxxji,T,;nUCLQQwpddppqqmmQLCYT ,,tTTTTTTTl       ";
echo " .tt!!l  irxxXcnnT::FYCLCuxxnnnxjrrrrYUvI.;TfTttTTTtI       ";
echo " Ittt!, ,fcnxJQmCfiIvULwwunnxxxxrxxnnLCLf:;xvxrT!tt!.       ";
echo " . ;tI:jCdppUwdqXlltcQmmwJunvvvuuvuuzQLQciiIYYcT!TJYt,      ";
echo "    FJQkhkkbbdwCjlIxwppdpwcvvvzYvcczwppmCjIIxJXJQqddbwY.    ";
echo "   taoahhhdYTllll!jnFfjxnnncCmLQLCJYUULmvnnF!l!Tnqkkbbbp.   ";
echo "  IXpahhpct!llll!!!!rT!!!!ttfcrcrf!!!!Fvx!lllllIIIjQddXut   ";
echo " .YcvYbqctllllllll!lljt!!!tttrjjf!l!!FvjllllllllIIijUjctcT  ";
echo ".JaCTvfYjlIIIlIlll!llTjl!tf!fjxfTFvrtxFllllllllIIIiInjrpdJj.";
echo "idbpLr!FFIIIIIIllllll!Tl!TTtjFjffft!IIIlllllllIIIIiITnJvuYqC";
echo " ixxI!fTrlIIIIIIIIIllIiiiIIIll!T!;iliIIlllllIIiiIiilrrUUwpqL";
echo "   :jjFTtlIIIIIIIIIIIIiiIIii!IIIl;IliiiiIIIIIIiiiiITttfxcxT,";
echo "    fzufF!IiIIIIIIiii;;IFrlllIlTTlIliiiiiiiiiiii;;iltTFji   ";
echo "    .cl  ,I;;iiiiIIi;;iiIljJXxxzztiiiiiIiii;;;;;;i.  ljx;   ";
echo "           iI;;;;;;;iiiI:      . .:iii;;;;;;;;;;;           ";
echo "             ,ii;;;;:.              .:;ii;;;;;,             ";
echo -e "\n${NC}"
echo "Enjoy the uma gifs."
exit 0