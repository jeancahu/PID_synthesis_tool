
if test -r $HOME/.pid_ss.conf
then DEFAULT_CONFIG_FILE="$HOME/.pid_ss.conf"
else
    printf "Please run config script" >/dev/stderr ; exit 1
fi

function define_from_config () {
    # $1 config name var
    # $2 bash format name
    eval $2="$(
	grep ^$1 $DEFAULT_CONFIG_FILE |
	    cut -f 2
	 )"
}
