#!/bin/bash

# Exemplos de requests
# curl -v -XPOST -H "content-type: application/json" -d '{"apelido" : "xpto", "nome" : "xpto xpto", "nascimento" : "2000-01-01", "stack": null}' "http://localhost:9999/pessoas"
# curl -v -XGET "http://localhost:9999/pessoas/1"
# curl -v -XGET "http://localhost:9999/pessoas?t=xpto"
# curl -v "http://localhost:9999/contagem-pessoas"

if [ $# -ne 1 ]; then
    echo "Usage: $0 <gatling install directory>"
    exit 1
fi

gatling_install_directory="$1"
gatling_shell="$gatling_install_directory/bin/gatling.sh"

if [ ! -f "$gatling_shell" ]; then
    echo "Invalid gatling install directory: $gatling_install_directory"
    exit -1
fi


this_script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
workspace_path="$this_script_dir/"

if [ ! -d "$workspace_path" ]; then
    echo "Invalid workspace directory: $workspace_path"
    exit -1
fi

sh "$gatling_shell" -rm local -s RinhaBackendSimulation \
	-rd  "DESCRICAO" \
	-rf  "$workspace_path/user-files/results" \
	-sf  "$workspace_path/user-files/simulations" \
	-rsf "$workspace_path/user-files/resources" \

sleep 3

curl -v "http://localhost:9999/contagem-pessoas"
