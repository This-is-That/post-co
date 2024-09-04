let imageIdToRemove = null; // 삭제할 이미지 ID를 저장할 변수
let selectedItems = []; // 선택된 항목들을 추적할 배열
let isEditMode = false;

// 팝업 요소와 버튼을 가져옵니다
const deletePopup = document.getElementById('deletePopup');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
const imageRemovedPopup = document.getElementById('imageRemovedPopup');
const generateButton = document.getElementById('generateButton');
const generatePopup = document.getElementById('generatePopup');
const confirmGenerateBtn = document.getElementById('confirmGenerateBtn');
const cancelGenerateBtn = document.getElementById('cancelGenerateBtn');
const promptInput = document.getElementById('promptInput');
const resetButton = document.getElementById('resetButton');
const deleteButton = document.getElementById('deleteButton');
const noImageMessage = document.getElementById('noImageMessage');
const selectedImage = document.getElementById('selectedImage');
const exampleMessage = document.getElementById('exampleMessage');

// 텍스트 입력란의 입력이 변경될 때 버튼의 활성화 상태를 업데이트합니다
function updateGenerateButtonState() {
    if (promptInput.value.trim() === '') {
        // 텍스트 입력란이 비어 있는 경우 버튼을 비활성화
        confirmGenerateBtn.disabled = true;
        // 클래스 업데이트: 비활성화된 상태의 스타일 적용
        confirmGenerateBtn.classList.remove('bg-blue-600', 'hover:bg-blue-700');
        confirmGenerateBtn.classList.add('bg-gray-500', 'hover:bg-gray-500');
        confirmGenerateBtn.style.cursor = 'not-allowed'; // 커서를 'not-allowed'로 변경
    } else {
        // 텍스트 입력란에 내용이 있는 경우 버튼을 활성화
        confirmGenerateBtn.disabled = false;
        // 클래스 업데이트: 활성화된 상태의 스타일 적용
        confirmGenerateBtn.classList.remove('bg-gray-500', 'hover:bg-gray-500');
        confirmGenerateBtn.classList.add('bg-blue-600', 'hover:bg-blue-700');
        confirmGenerateBtn.style.cursor = 'pointer'; // 커서를 'pointer'로 변경
    }
}

promptInput.addEventListener('input', updateGenerateButtonState);

// 팝업을 표시하는 함수
function showDeletePopup() {
    deletePopup.classList.add('visible');
}

function showGeneratePopup() {
    generatePopup.classList.add('visible');
}

// 팝업을 숨기는 함수
function hideDeletePopup() {
    deletePopup.classList.remove('visible');
}

function hideGeneratePopup() {
    generatePopup.classList.remove('visible');
}

// 삭제 완료 메시지 팝업 표시 함수
function showImageRemovedPopup() {
    imageRemovedPopup.classList.add('visible');
    setTimeout(() => {
        imageRemovedPopup.classList.remove('visible');
    }, 1500); // 1.5초 동안 표시
}

// Reset 버튼 클릭 시 호출되는 함수
function handleResetButtonClick() {
    selectedItems.forEach(item => {
        item.element.classList.remove('selected');
        item.element.querySelector('.checkmark').textContent = ''; // 체크마크 내용 초기화
    });
    selectedItems = []; // 선택된 항목 배열 초기화

    // Generate 버튼 상태 업데이트
    toggleGenerateButton();
    updateSelectedCount();

    // Reset 버튼 상태 업데이트
    resetButton.disabled = true;
    resetButton.style.backgroundColor = '#66bb6a'; // 초록색
    resetButton.style.color = 'white';
    resetButton.style.cursor = 'not-allowed';
    resetButton.style.opacity = '0.5';

    // Delete 버튼 상태 업데이트
    deleteButton.disabled = true;
    deleteButton.style.backgroundColor = '#ef5350'; // 빨간색
    deleteButton.style.color = 'white';
    deleteButton.style.cursor = 'not-allowed';
    deleteButton.style.opacity = '0.5';

    // 로컬 스토리지에서 저장된 선택된 항목이 있다면 제거
    localStorage.removeItem('selectedItems');
}

// Delete 버튼 클릭 시 호출되는 함수
function handleDeleteButtonClick() {
    if (selectedItems.length > 0) {
        showDeletePopup(); // 삭제 확인 팝업 표시
    }
}

// Confirm Delete 버튼 클릭 시 호출되는 함수
function confirmDelete() {
    selectedItems.forEach(item => {
        removeFromCart(item.id);
    });
    selectedItems = []; // 삭제 후 선택된 항목 배열 초기화

    hideDeletePopup();
    showImageRemovedPopup(); // 삭제 완료 메시지 표시
    toggleGenerateButton(); // Generate 버튼 상태 업데이트
    toggleActionButtons(); // Action 버튼 상태 업데이트
    updateSelectedCount();
}

// Remove from cart 함수
function removeFromCart(id) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => item.id !== id);
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCartItems();
}

// Action 버튼 상태 업데이트 함수
function toggleActionButtons() {
    if (selectedItems.length > 0) {
        resetButton.disabled = false;
        resetButton.style.backgroundColor = '#4caf50'; // 초록색
        resetButton.style.color = 'white';
        resetButton.style.cursor = 'pointer';
        resetButton.style.opacity = '1';

        deleteButton.disabled = false;
        deleteButton.style.backgroundColor = '#e53935'; // 빨간색
        deleteButton.style.color = 'white';
        deleteButton.style.cursor = 'pointer';
        deleteButton.style.opacity = '1';
    } else {
        resetButton.disabled = true;
        resetButton.style.backgroundColor = '#66bb6a'; // 비활성화 색상 (초록색)
        resetButton.style.color = 'white';
        resetButton.style.cursor = 'not-allowed';
        resetButton.style.opacity = '0.5';

        deleteButton.disabled = true;
        deleteButton.style.backgroundColor = '#ef5350'; // 비활성화 색상 (빨간색)
        deleteButton.style.color = 'white';
        deleteButton.style.cursor = 'not-allowed';
        deleteButton.style.opacity = '0.5';
    }
}

// 확인 버튼 클릭 시 이미지 삭제
confirmDeleteBtn.addEventListener('click', function() {
    if (imageIdToRemove !== null) {
        removeFromCart(imageIdToRemove);
        hideDeletePopup();
        showImageRemovedPopup(); // 삭제 완료 메시지 표시
        selectedItems = [];
        updateSelectedCount();
    }
});

// 취소 버튼 클릭 시 팝업 숨기기
cancelDeleteBtn.addEventListener('click', function() {
    hideDeletePopup();
});

// Generate 버튼 클릭 시 팝업 표시
generateButton.addEventListener('click', () => {
    const checkId = document.getElementById('checkId');
    const rawKopisGenId = window.kopisGenId;
    const kopisGenId = rawKopisGenId.replace(/"/g, '');

    if (checkId.value !== kopisGenId) {
        console.error('Error: The input value is not correct');
        return; // 조건을 만족하지 않으면 아래 코드를 실행하지 않음
    }

    showGeneratePopup(); // 팝업 표시
    const generatePopupTitle = document.getElementById('generatePopupTitle');
    generatePopupTitle.innerText = '나만의 포스터를 만들어요!';
    // 선택된 이미지를 보여주는 함수
    const selectedItemsData = selectedItems.map(item => ({
        id: item.id,
        url: item.element.querySelector('img').src
    }));

    // 선택된 이미지의 첫 번째 항목을 가져와서 이미지 요소에 설정
    if (selectedItemsData.length > 0) {
        const selectedImage = document.getElementById('selectedImage');
        selectedImage.src = selectedItemsData[0].url;
        selectedImage.classList.remove('hidden');
        noImageMessage.classList.add('hidden');
        exampleMessage.classList.remove('hidden')
    }
    else {
        selectedImage.classList.add('hidden');
        noImageMessage.classList.remove('hidden');
        exampleMessage.classList.add('hidden')
    }
});

function updateSelectedCount() {
    const selectedCountElement = document.getElementById('selectedCount');
    selectedCountElement.textContent = `Selected: ${selectedItems.length}`;
}

function toggleSelection(event) {
    const wrapper = event.currentTarget;
    const id = wrapper.querySelector('img').dataset.id;

    if (wrapper.classList.contains('selected')) {
        wrapper.classList.remove('selected');
        selectedItems = selectedItems.filter(item => item.id !== id);
        wrapper.querySelector('.checkmark').textContent = ''; // 체크마크 내용 초기화
    } else {
        wrapper.classList.add('selected');
        selectedItems.push({ id, element: wrapper });
        wrapper.querySelector('.checkmark').textContent = selectedItems.length; // 체크마크에 번호 부여
    }

    updateSelectionOrder();
    updateSelectedCount(); // 선택 상태 변경 시 선택 항목 수 업데이트
    toggleGenerateButton(); // Generate 버튼 상태 업데이트
    toggleActionButtons(); // Action 버튼 상태 업데이트
}

function updateSelectionOrder() {
    selectedItems.forEach((item, index) => {
        item.element.querySelector('.checkmark').textContent = index + 1; // 1부터 시작하는 번호 부여
    });
}

function toggleGenerateButton() {
    if (selectedItems.length < 2) {
        generateButton.disabled = false;
        // 클래스 업데이트: 활성화된 상태의 스타일 적용
        generateButton.classList.remove('bg-gray-400', 'cursor-not-allowed');
        generateButton.classList.add('bg-blue-600', 'cursor-pointer');
    } else {
        generateButton.disabled = true;
        // 클래스 업데이트: 비활성화된 상태의 스타일 적용
        generateButton.classList.remove('bg-blue-600', 'cursor-pointer');
        generateButton.classList.add('bg-gray-400', 'cursor-not-allowed');
    }
}

// Generate 확인 버튼 클릭 시 요청 보내기
confirmGenerateBtn.addEventListener('click', () => {
    const promptText = document.getElementById('promptInput').value;
    const selectedImage = document.getElementById('selectedImage');
    
    hideGeneratePopup(); // 생성 팝업 숨기기
    showLoadingPopup(); // 로딩 팝업 표시

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: promptText, selectedItem: selectedImage.src})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        hideLoadingPopup(); // 로딩 팝업 숨기기

        if (data && data.gen_image_urls) {
            // 이미지 URL을 로컬 스토리지에 저장
            localStorage.setItem('generatedImages', JSON.stringify(data.gen_image_urls));
            displayGeneratedImages(data.gen_image_urls);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        hideLoadingPopup(); // 에러 발생 시에도 로딩 팝업 숨기기
        // 에러 처리 (예: 에러 메시지 표시)
    });
});

// Generate 취소 버튼 클릭 시 팝업 숨기기
cancelGenerateBtn.addEventListener('click', function() {
    hideGeneratePopup();
});

// 페이지 로드 시 장바구니 아이템 표시
window.onload = () => {
    displayCartItems();
    updateGenerateButtonState(); // 페이지 로드 시 Generate 버튼 상태 초기화
    toggleActionButtons(); // 페이지 로드 시 Action 버튼 상태 초기화
    
    // 선택 항목 수 초기화
    updateSelectedCount();

    // 로컬 스토리지에서 생성된 이미지 URL 가져오기
    const storedGeneratedImages = JSON.parse(localStorage.getItem('generatedImages'));
    if (storedGeneratedImages) {
        displayGeneratedImages(storedGeneratedImages);
    }

    setTimeout(function() {
        window.scrollTo(0, 0);
    }, 0);
};

// 장바구니 항목을 표시하는 함수
function displayCartItems() {
    const cartItems = document.getElementById('cartItems');
    const cart = JSON.parse(localStorage.getItem('cart')) || [];

    cartItems.innerHTML = ''; // 초기화
    selectedItems = []; // 선택된 항목 초기화
    toggleGenerateButton(); // Generate 버튼 상태 초기화
    toggleActionButtons(); // Action 버튼 상태 초기화

    cart.forEach(item => {
        const wrapper = document.createElement('div');
        wrapper.classList.add('image-wrapper');
        wrapper.onclick = toggleSelection;

        const imgElement = document.createElement('img');
        imgElement.src = item.src;
        imgElement.alt = 'Cart Item';
        imgElement.classList.add('w-full', 'h-auto', 'rounded-t-lg', 'shadow');
        imgElement.dataset.id = item.id;

        const infoDiv = document.createElement('div');
        infoDiv.classList.add('image-info');
        infoDiv.innerHTML = `
            <p><strong>Title:</strong> ${item.info?.image_id || 'N/A'}</p>
            <p><strong>Start Date:</strong> ${item.info?.start_date || 'N/A'}</p>
            <p><strong>End Date:</strong> ${item.info?.end_date || 'N/A'}</p>
            <p><strong>Place Name:</strong> ${item.info?.place_name || 'N/A'}</p>
            <p><strong>Actor:</strong> ${item.info?.actor || 'N/A'}</p>
            <p><strong>Runtime:</strong> ${item.info?.runtime || 'N/A'}</p>
            <p><strong>Age:</strong> ${item.info?.age || 'N/A'}</p>
        `;

        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'X';
        removeBtn.classList.add('remove-btn');
        removeBtn.onclick = () => showDeletePopup(item.id);

        const checkmark = document.createElement('div');
        checkmark.classList.add('checkmark');
        checkmark.innerHTML = ''; // 빈 체크마크

        wrapper.appendChild(imgElement);
        wrapper.appendChild(infoDiv);
        wrapper.appendChild(removeBtn);
        wrapper.appendChild(checkmark);

        cartItems.appendChild(wrapper);
    });
}

// 생성 이미지 섹션을 표시하는 함수
function displayGeneratedImages(imageUrls) {
    const genImageSection = document.getElementById('genImageSection');
    const generatedImages = document.getElementById('generatedImages');
    generatedImages.innerHTML = ''; // 기존 이미지 제거

    if (imageUrls && imageUrls.length > 0) {
        imageUrls.forEach((url, index) => {
            const wrapper = document.createElement('div');
            wrapper.classList.add('image-wrapper');

            const imgElement = document.createElement('img');
            imgElement.src = url;
            imgElement.alt = `Generated Image ${index + 1}`;
            
            const editBtn = document.createElement('button');
            editBtn.textContent = '👨‍🎨 Edit';
            editBtn.classList.add('mt-2', 'bg-blue-600', 'text-white', 'px-4', 'py-2', 'rounded-lg', 'hover:bg-blue-700');
            editBtn.onclick = () => {
                showGeneratePopup();
                const selectedImage = document.getElementById('selectedImage');
                const generatePopupTitle = document.getElementById('generatePopupTitle');
                generatePopupTitle.innerText = '생성한 포스터를 다시 수정할 수 있어요!';
                selectedImage.src = url;
                selectedImage.classList.remove('hidden');
                noImageMessage.classList.add('hidden');
                exampleMessage.classList.remove('hidden');
            }

            const downloadBtn = document.createElement('button');
            downloadBtn.textContent = '📥 Download';
            downloadBtn.classList.add('mt-2', 'bg-blue-600', 'text-white', 'px-4', 'py-2', 'mb-20', 'rounded-lg', 'hover:bg-blue-700');
            downloadBtn.onclick = () => showDownloadPopup(url);

            wrapper.appendChild(imgElement);
            wrapper.appendChild(editBtn);
            wrapper.appendChild(downloadBtn);
            generatedImages.appendChild(wrapper);
        });
        
        genImageSection.classList.remove('hidden');
        genImageSection.style.display = 'flex';

        genImageSection.scrollIntoView({ behavior: 'smooth' , block: 'start'});
    } else {
        genImageSection.classList.add('hidden');
        genImageSection.style.display = 'none';
    }
}

// 다운로드 팝업 보여주기
function showDownloadPopup(url) {
    const downloadPopup = document.getElementById('downloadPopup');
    downloadPopup.classList.add('visible');

    const confirmDownloadBtn = document.getElementById('confirmDownloadBtn');
    confirmDownloadBtn.onclick = () => {
        downloadImage(url);
        downloadPopup.classList.remove('visible');
        showDownloadSuccessPopup();
    };

    const cancelDownloadBtn = document.getElementById('cancelDownloadBtn');
    cancelDownloadBtn.onclick = () => {
        downloadPopup.classList.remove('visible');
    };
}

// 이미지 다운로드 성공 팝업
function showDownloadSuccessPopup() {
    const downloadSuccessPopup = document.getElementById('downloadSuccessPopup');
    downloadSuccessPopup.classList.add('visible');

    setTimeout(() => {
        downloadSuccessPopup.classList.remove('visible');
    }, 2000); // 2초 후에 팝업 숨기기
}

function showLoadingPopup() {
    document.getElementById('loadingPopup').classList.remove('hidden');
}

function hideLoadingPopup() {
    document.getElementById('loadingPopup').classList.add('hidden');
}

// 이미지 다운로드 함수
function downloadImage(url) {
    fetch(url, { method: 'GET', mode: 'cors' }) // mode: 'cors'로 CORS 요청을 시도
        .then(response => {
            if (response.ok) {
                // CORS 오류가 없을 경우, Blob을 사용하여 다운로드 처리
                return response.blob();
            } else {
                // CORS 오류 외에 다른 HTTP 오류가 발생할 경우 처리
                throw new Error('Network response was not ok.');
            }
        })
        .then(blob => {
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = url.split('/').pop(); // 파일 이름 설정
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => {
            console.error('Download failed:', error);
            // CORS 오류 또는 기타 오류 발생 시, 다운로드 링크를 새 창에서 열기
            const link = document.createElement('a');
            link.href = url;
            link.download = url.split('/').pop(); // 파일 이름 설정
            link.target = '_blank'; // 새 창에서 열기
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
}

// 페이지 상단으로 스크롤 기능 구현
document.getElementById('scrollToTopBtn').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth'});
});

document.getElementById('copyButton').addEventListener('click', function (event) {
    const emailText = document.getElementById('emailText').innerText;
    navigator.clipboard.writeText(emailText).then(() => {
        const copyButton = event.target;
        const buttonRect = copyButton.getBoundingClientRect();
        const popup = document.getElementById('copyPopup');
        popup.style.left = `${buttonRect.left + buttonRect.width / 2}px`;
        popup.style.top = `${buttonRect.bottom + 10}px`;
        popup.classList.remove('hidden');
        setTimeout(() => {
            popup.classList.add('hidden');
        }, 1500);
    }).catch(err => {
        console.error('Could not copy text: ', err);
    });
});

// 스크롤 시 버튼 표시 제어
window.addEventListener('scroll', () => {
    const scrollToTopBtn = document.getElementById('scrollToTopBtn');
    if (window.scrollY > 300) { // 페이지 스크롤이 300px 이상일 때 버튼 표시
        scrollToTopBtn.classList.remove('hidden');
    } else {
        scrollToTopBtn.classList.add('hidden');
    }
});

// Reset 버튼 클릭 이벤트 리스너 추가
resetButton.addEventListener('click', handleResetButtonClick);

// Delete 버튼 클릭 이벤트 리스너
deleteButton.addEventListener('click', handleDeleteButtonClick);

// Confirm Delete 버튼 클릭 이벤트 리스너
confirmDeleteBtn.addEventListener('click', confirmDelete);

// Cancel Delete 버튼 클릭 이벤트 리스너
cancelDeleteBtn.addEventListener('click', () => {
    hideDeletePopup();
});