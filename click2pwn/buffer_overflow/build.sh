if [ -z $1 ]; then
	echo "Usage: ./build.sh [shellcode file]"
	exit 1
fi

tool_chain=arm-linux-gnueabihf

mkdir -p build && \
$tool_chain-as $1 -o build/payload.o && \
$tool_chain-ld.bfd build/payload.o -o build/payload && \
$tool_chain-objcopy -O binary --only-section=.text ./build/payload ./payload.bin
