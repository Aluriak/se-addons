# Convertion of local music files to ogg.
#  Delete source files

for f in *.{mp3,flac,mp4,wav}
do
    name=$(basename "${f}")
    extn="${name##*.}"
    name="${name%.*}"
    source="${name}.${extn}"
    target="${name}.ogg"
    ffmpeg -i "${source}" "${target}" -n
    rm "${source}"
done
echo "DONE"
