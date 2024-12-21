document.addEventListener('DOMContentLoaded',  async () => {
    const textElement = document.getElementById('carouselContent');
    const paragraphs = textElement.getElementsByTagName('p');
    const documentId = document.getElementById('documentId').value;
    const selectedList = document.getElementById('selectedList');
    const currentSelection = document.getElementById('currentSelection');
    const currentSelectionList = document.getElementById('currentSelectionList');
    const cancelButton = document.getElementById('cancelButton');
    const prevButton = document.getElementById('prevBtn');
    const nextButton = document.getElementById('nextBtn');
    const nbPage = document.getElementById('nbPage');
    const entities = document.getElementById('entitiesList').value.split(',');
    const verbs = document.getElementById('verbList').value.split(',');
    const nextDocButton = document.getElementById('nextDocument');
    const nextDocumentUrl = document.getElementById('nextDocumentUrl') ? document.getElementById('nextDocumentUrl').value : null;
    const nextDocumentBtn = document.getElementById('nextDocumentBtn');

    let dirHandle = null;
    let isDownloaded = false; // Flag to check if download has been done
    let premiersMots = [];
    let currentParagraph = 0;
    let selectionCount = 0;
    let selectedPhrases = [];
    let paragraphID = "None";

    // Check if the document is already downloaded
    if (localStorage.getItem(`downloaded_${documentId}`) === 'true') {
        isDownloaded = true;
    }
    
    async function downloadFile() {
        const phrases = Array.from(selectedList.children).map(li => li.firstChild.textContent);
        const blob = new Blob([phrases.join('\n')], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        //a.download = path.join('annotated_documents',  'Annotation_doc_'+${documentId}+'.txt');
        a.download = `Annotation_${documentId}.txt`; // Set the file name with document ID
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        // Mark the document as downloaded in localStorage
        localStorage.setItem(`downloaded_${documentId}`, true);
        isDownloaded = true;  // Mark as downloaded after saving
    }

    async function autoDownloadIfNotDone() {
        console.log(isDownloaded);
        if (!isDownloaded) {
            await downloadFile();  // Automatically download the file if not done manually
            isDownloaded = true;  // Mark as downloaded
            alert("Annotation downloaded!\nRedirecting to the next document...");
        }
        if (nextDocumentUrl) {
            window.location.href = nextDocumentUrl;
        }
    }


    function highlightEntities() {
        Array.from(paragraphs).forEach(paragraph => {
            let text = paragraph.innerHTML;
            entities.forEach(entity => {
                const regex = new RegExp(`(${entity})`, 'gi');
                text = text.replace(regex, `<span class="highlighted">$1</span>`);
                //console.log(text)
            });
            paragraph.innerHTML = text;
        });
    }

    function colorVerbs() {
        let text = textElement.innerHTML;
        verbs.forEach(verb => {
            const regex = new RegExp(`(${verb})`, 'gi');
            text = text.replace(regex, `<span class="colored">$1</span>`);
        });
        textElement.innerHTML = text;
    }

    function colorParag(){
        let text = textElement.innerHTML;
        //premiersMots = premiersMots.reverse();
        premiersMots.forEach(mot => {
            const regex = new RegExp(`(${mot}) `, 'gi');
            //console.log(regex)
            text = text.replace(regex, `<span class="underline">$&</span>`);

        });
        //console.log(premiersMots)
        textElement.innerHTML = text;
    }

    function showParagraph(index) {
        for (let i = 0; i < paragraphs.length; i++) {
            paragraphs[i].style.display = i === index ? 'block' : 'none';
            if (i === index ){
                paragraphID = 'p'+(i+1);
            }
            //idParagraph = paragraphs[i]["id"]

            let text = paragraphs[i].innerText || paragraphs[i].textContent;

            let mots = text.split(' ');
            let premierMot = mots.shift();
            //console.log(premierMot)
            premiersMots.push(premierMot);

            // Show "Next Document" button only on the last paragraph
            if (index === paragraphs.length - 1 && nextDocumentUrl) {
                nextDocumentBtn.style.display = 'inline-block';
            } else {
                nextDocumentBtn.style.display = 'none';
            }

        }
        nbPage.innerText = (index +1) + "/"+ paragraphs.length
        if (index == 0) {
            prevButton.style.background = "grey";
        }
        else
            prevButton.style.background = "blue";

        if(index == paragraphs.length-1){
            nextButton.style.background = "grey";
        }
        else
            nextButton.style.background = "blue";
    }

    function nextParagraph() {
        if (currentParagraph < paragraphs.length - 1) {
            currentParagraph++;
            showParagraph(currentParagraph);

        }
    }

    function prevParagraph() {
        if (currentParagraph > 0) {
            currentParagraph--;
            showParagraph(currentParagraph);
        }

    }

    function startSelection() {
        selectionCount = 0;
        selectedPhrases = [];
        currentSelectionList.innerHTML = '';
        currentSelection.style.display = 'block';
        cancelButton.style.display = 'inline-block';
        textElement.addEventListener('dblclick', selectPhrase);
    }

    function selectPhrase(event) {
        if (event.target.classList.contains('highlighted') || event.target.classList.contains('colored')) {
            const selectedText = event.target.innerText.trim();

            if (selectedText && selectionCount < 3) {
                selectedPhrases.push(selectedText);
                selectionCount++;

                updateCurrentSelection();

                if (selectionCount === 3 ) {
                    addPhraseToList();
                    textElement.removeEventListener('dblclick', selectPhrase);
                    currentSelection.style.display = 'none';
                    cancelButton.style.display = 'none';
                }
            }
        }
        //premiersMots = premiersMots.reverse();
        if (event.target.classList.contains('underline')) {
            const selectedText = event.target.innerText.trim();
            console.log(premiersMots)
            if (selectedText && selectionCount < 1) {
                selectedPhrases.push(selectedText);
                selectionCount++;

                updateCurrentSelection();

                if (selectionCount === 1 ) {
                    addPhraseToList();
                    textElement.removeEventListener('dblclick', selectPhrase);
                    currentSelection.style.display = 'none';
                    cancelButton.style.display = 'none';
                }
            }
        }
    }

    function updateCurrentSelection() {
        currentSelectionList.innerHTML = '';
        selectedPhrases.forEach(phrase => {
            const li = document.createElement('li');
            li.textContent = phrase;
            currentSelectionList.appendChild(li);
        });
    }

    function addPhraseToList() {
        const li = document.createElement('li');
        const span = document.createElement('span');
        span.textContent = paragraphID+", "+selectedPhrases.join(', ');

        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'Remove';
        removeBtn.addEventListener('click', () => {
            selectedList.removeChild(li);
        });

        li.appendChild(span);
        li.appendChild(removeBtn);
        selectedList.appendChild(li);
    }

    function cancelSelection() {
        selectionCount = 0;
        selectedPhrases = [];
        currentSelectionList.innerHTML = '';
        currentSelection.style.display = 'none';
        cancelButton.style.display = 'none';
        textElement.removeEventListener('dblclick', selectPhrase);
    }


    highlightEntities();
    showParagraph(currentParagraph);
    colorVerbs();
    //colorParag();

    window.startSelection = startSelection;
    window.cancelSelection = cancelSelection;
    window.downloadFile = downloadFile;
    window.nextParagraph = nextParagraph;
    window.prevParagraph = prevParagraph;
    window.goToNextDocument = autoDownloadIfNotDone;

    

});
