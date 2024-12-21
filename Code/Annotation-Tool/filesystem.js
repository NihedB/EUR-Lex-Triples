$(document).ready(function () {
    let dirHandle; // Store the selected directory handle globally
    let isDownloaded = false; // Flag to check if download has been done

    $('#selectFolderBtn').click(async function () {
        localStorage.clear();
        // Use File System Access API to allow the user to select a folder
        try {
            dirHandle = await window.showDirectoryPicker();  // User selects the folder

            // Read the contents of the selected directory
            const filesList = $('#downloadedFilesList');
            filesList.empty(); // Clear any previous list items
            console.log(dirHandle);
            
            for await (const entry of dirHandle.values()) {
                if (entry.kind === 'file') {
                    const fileName = entry.name;

                    // Check if the file is one of the expected downloaded files
                    if (fileName.startsWith('Annotation_')) {
                        //const listItem = $('<li>').text(fileName);
                        //filesList.append(listItem);

                        // Add a checkmark next to matching document links
                        const Id = fileName.split('_')[2].split('.')[0]; 
                        const docId = fileName.replace(fileName.split('_')[0]+"_", "").split(".")[0]; 
                        console.log("docId : ", docId)
                        $(`a[data-id="${docId}"]`).addClass('downloaded').append(' ✅');
                        localStorage.setItem(`downloaded_${docId}`, true);
                    }
                }
            }
            
        } catch (err) {
            console.error('Error accessing file system:', err);
        }
    });

    // Function to download annotations automatically if not downloaded before navigating to the next document
    async function autoDownloadIfNotDone() {
        if (!isDownloaded) {
            await downloadFile();  // Automatically download the file
            isDownloaded = true;  // Mark as downloaded
        }
        let nextDocumentUrl = $('#nextDocumentUrl').val();
        if (nextDocumentUrl) {
            window.location.href = nextDocumentUrl;
        }
    }


     // Add a "Next" button behavior for navigation between paragraphs
    $('#nextDocumentBtn').click(function () {
        autoDownloadIfNotDone();  // Trigger the auto-download if needed
    });
    
    
});

