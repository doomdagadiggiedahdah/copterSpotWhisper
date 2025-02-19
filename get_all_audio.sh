#!/bin/bash

TARBALL_LIST="./data/tarball_links.txt"
DOWNLOAD_DIR="./data/tarballs"
EXTRACT_DIR="./data/extracted"
NUM_WORKERS=4  # Set number of workers

mkdir -p "$DOWNLOAD_DIR" "$EXTRACT_DIR"

cat "$TARBALL_LIST" | xargs -P 8 -I {} wget {} -P "$DOWNLOAD_DIR"

mkdir -p "$EXTRACT_DIR"
find "$DOWNLOAD_DIR" -name "*.tar.gz" | \
  xargs -P 8 -I {} tar xf {} -C "$EXTRACT_DIR"


# -------------------- #
# **DISTRIBUTE FILES** #
# -------------------- #

# # Create worker directories
# for i in $(seq 0 $((NUM_WORKERS - 1))); do
#     mkdir -p "$EXTRACT_DIR/$i"
# done

# # Get list of all extracted files
# mapfile -t FILES < <(find "$EXTRACT_DIR" -type f -name "*.mp3")

# TOTAL_FILES=${#FILES[@]}
# FILES_PER_WORKER=$((TOTAL_FILES / NUM_WORKERS))
# EXTRA_FILES=$((TOTAL_FILES % NUM_WORKERS)) # Handle remaining files

# echo "Total files: $TOTAL_FILES"
# echo "Files per worker: $FILES_PER_WORKER (+$EXTRA_FILES extra files)"

# # Move files into worker directories
# index=0
# for i in $(seq 0 $((NUM_WORKERS - 1))); do
#     COUNT=$FILES_PER_WORKER
#     [[ $i -lt $EXTRA_FILES ]] && COUNT=$((COUNT + 1))  # Distribute extra files
    
#     for j in $(seq 1 $COUNT); do
#         [[ $index -ge $TOTAL_FILES ]] && break
#         mv "${FILES[index]}" "$EXTRACT_DIR/$i/"
#         ((index++))
#     done
# done

# echo "Files successfully distributed across $NUM_WORKERS workers!"


# #!/bin/bash

# TARBALL_LIST="./data/tarball_links.txt"
# DOWNLOAD_DIR="./data/tarballs"
# EXTRACT_DIR="./data/extracted"

# mkdir -p "$DOWNLOAD_DIR" "$EXTRACT_DIR"

# # Function to download and extract a tarball
# download_and_extract() {
#     local url="$1"
#     local filename=$(basename "$url")
#     local tar_path="$DOWNLOAD_DIR/$filename"

#     # Download the tarball
#     echo "Downloading: $url"
#     curl -L "$url" -o "$tar_path"

#     # Extract using pigz
#     echo "Extracting: $filename"
#     pigz -dc "$tar_path" | tar xv -C "$EXTRACT_DIR" --no-same-owner > /dev/null 2>&1

#     echo "Finished: $filename"
# }

# # Read URLs from file and process them one by one
# while IFS= read -r url; do
#     download_and_extract "$url"
# done < "$TARBALL_LIST"

# echo "All tarballs processed!"