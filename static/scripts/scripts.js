document.getElementById('file-upload').addEventListener('change', function() {
    const filesList = document.getElementById('uploaded-files');
    filesList.innerHTML = '';  // Clear previous file names

    for (let file of this.files) {
        const fileItem = document.createElement('div');
        fileItem.innerHTML = `<i class="fas fa-check"></i> ${file.name}`;
        filesList.appendChild(fileItem);
    }
});