const getStartedBtn = document.getElementById('getStartedBtn');
const searchInput = document.getElementById('searchInput');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const dropArea = document.getElementById('dropArea');
const imageContainer = document.getElementById('imageContainer');
const cartItems = document.getElementById('cartItems');
const clearInputBtn = document.getElementById('clearInputBtn');
const deletePopup = document.getElementById('deletePopup');
const addToCartPopup = document.getElementById('addToCartPopup');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
const confirmAddToCartBtn = document.getElementById('confirmAddToCartBtn');
const cancelAddToCartBtn = document.getElementById('cancelAddToCartBtn');
let isRequesting = false;
let imageToDelete = null;
let imageToAdd = null;

function toggleGetStartedButton() {
    const isEnabled = searchInput.value.trim().length > 0;
    getStartedBtn.disabled = !isEnabled;
    getStartedBtn.classList.toggle('bg-blue-600', isEnabled);
    getStartedBtn.classList.toggle('hover:bg-blue-700', isEnabled);
    getStartedBtn.classList.toggle('bg-gray-400', !isEnabled);
    getStartedBtn.classList.toggle('cursor-not-allowed', !isEnabled);
    getStartedBtn.classList.toggle('cursor-pointer', isEnabled);

    // Clear button visibility toggle
    clearInputBtn.classList.toggle('hidden', !isEnabled);
}

function showLoadingPopup() {
    document.getElementById('loadingPopup').classList.remove('hidden');
}

function hideLoadingPopup() {
    document.getElementById('loadingPopup').classList.add('hidden');
}

function displayImages(imageLinks, imageIds, imageInfos) {
    hideLoadingPopup();
    isRequesting = false;

    // 검색 결과 텍스트를 숨기기 전에 숨김 처리
    const searchResultsText = document.querySelector('#imageResults h3');
    searchResultsText.classList.add('hidden');

    imageContainer.innerHTML = '';

    if (Array.isArray(imageLinks)) {
        imageLinks.forEach((link, index) => {
            const imgElement = document.createElement('img');
            imgElement.src = link;
            imgElement.alt = 'Search Result Image';
            imgElement.classList.add('w-full', 'h-auto', 'rounded-lg', 'shadow');
            imgElement.dataset.id = imageIds ? imageIds[index] : '';
            imgElement.dataset.info = imageInfos ? JSON.stringify(imageInfos[index]) : '';

            const infoDiv = document.createElement('div');
            infoDiv.classList.add('image-info');
            infoDiv.innerHTML = `
                <p><strong>Title:</strong> ${imageInfos[index]?.image_id || 'N/A'}</p>
                <p><strong>Start Date:</strong> ${imageInfos[index]?.start_date || 'N/A'}</p>
                <p><strong>End Date:</strong> ${imageInfos[index]?.end_date || 'N/A'}</p>
                <p><strong>Place Name:</strong> ${imageInfos[index]?.place_name || 'N/A'}</p>
                <p><strong>Actor:</strong> ${imageInfos[index]?.actor || 'N/A'}</p>
                <p><strong>Runtime:</strong> ${imageInfos[index]?.runtime || 'N/A'}</p>
                <p><strong>Age:</strong> ${imageInfos[index]?.age || 'N/A'}</p>
            `;

            let hideTimeout;

            // 이미지에 마우스 오버 시 infoDiv 보이기
            imgElement.addEventListener('mouseover', function () {
                clearTimeout(hideTimeout);
                infoDiv.style.display = 'block'; // display 설정
                requestAnimationFrame(() => {
                    infoDiv.style.opacity = '1';
                    infoDiv.style.transform = 'translateY(0)';
                });
            });

            // 이미지에서 마우스가 벗어날 때 infoDiv 숨기기 (딜레이)
            imgElement.addEventListener('mouseout', function () {
                hideTimeout = setTimeout(() => {
                    if (!imgElement.matches(':hover') && !infoDiv.matches(':hover')) {
                        infoDiv.style.opacity = '0';
                        infoDiv.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            if (!imgElement.matches(':hover') && !infoDiv.matches(':hover')) {
                                infoDiv.style.display = 'none'; // display 설정
                            }
                        }, 200); // 애니메이션 시간과 동일한 지연
                    }
                }, 200); // 200ms 후에 숨김
            });

            // infoDiv에 마우스 오버 시 숨기지 않기
            infoDiv.addEventListener('mouseover', function () {
                clearTimeout(hideTimeout);
                infoDiv.style.display = 'block'; // display 설정
                requestAnimationFrame(() => {
                    infoDiv.style.opacity = '1';
                    infoDiv.style.transform = 'translateY(0)';
                });
            });

            // infoDiv에서 마우스가 벗어날 때 숨기기 (딜레이)
            infoDiv.addEventListener('mouseout', function () {
                hideTimeout = setTimeout(() => {
                    if (!imgElement.matches(':hover') && !infoDiv.matches(':hover')) {
                        infoDiv.style.opacity = '0';
                        infoDiv.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            if (!imgElement.matches(':hover') && !infoDiv.matches(':hover')) {
                                infoDiv.style.display = 'none'; // display 설정
                            }
                        }, 200); // 애니메이션 시간과 동일한 지연
                    }
                }, 200); // 200ms 후에 숨김
            });

            const wrapper = document.createElement('div');
            wrapper.classList.add('relative');
            wrapper.appendChild(imgElement);
            wrapper.appendChild(infoDiv);

            // Add click event for adding to cart
            imgElement.addEventListener('click', function () {
                imageToAdd = imgElement;
                addToCartPopup.style.display = 'block';
            });

            imageContainer.appendChild(wrapper);
        });

        // Make the search results text visible after loading images
        Promise.all(Array.from(imageContainer.querySelectorAll('img')).map(img => {
            if (img.complete) return Promise.resolve();
            return new Promise(resolve => { img.onload = img.onerror = resolve; });
        })).then(() => {
            searchResultsText.classList.remove('hidden');
            document.getElementById('imageResults').scrollIntoView({ behavior: 'smooth' });
        });
    } else {
        console.error('Invalid image links format:', imageLinks);
        alert('서버에서 잘못된 형식의 응답을 받았습니다.');
    }
}

function addImageToCart(image) {
    const imageId = image.dataset.id;
    const imageSrc = image.src;
    const imageInfo = image.dataset.info ? JSON.parse(image.dataset.info) : {};

    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    const imageExists = cart.some(item => item.id === imageId);

    if (!imageExists) {
        cart.push({
            id: imageId,
            src: imageSrc,
            info: imageInfo
        });

        localStorage.setItem('cart', JSON.stringify(cart));
        showPopup('🛒 포스터가 장바구니에 추가되었습니다!', 'imageAddedPopup');
    } else {
        deletePopup.classList.add('visible');
        
        // 확인 버튼 클릭 시 장바구니에서 포스터 삭제
        confirmDeleteBtn.addEventListener('click', function() {
            // 장바구니에서 포스터 삭제 로직
            cart = cart.filter(item => item.id !== imageId);
            localStorage.setItem('cart', JSON.stringify(cart));
            deletePopup.classList.remove('visible'); // 팝업 숨기기

            // 삭제 완료 메시지 표시
            showPopup('👋 포스터가 장바구니에서 삭제되었습니다!', 'imageRemovedPopup');
        });

        // 취소 버튼 클릭 시 팝업 숨기기
        cancelDeleteBtn.addEventListener('click', function() {
            deletePopup.classList.remove('visible'); // 팝업 숨기기
        });
    }
}

function removeImageFromCart(imageId) {
    const images = cartItems.querySelectorAll('img');
    images.forEach(img => {
        if (img.dataset.id === imageId) {
            img.remove();
        }
    });
}

function sendPostRequest(data, isFileUpload = false) {
    const options = {
        method: 'POST',
        headers: isFileUpload ? {} : { 'Content-Type': 'application/json' },
        body: isFileUpload ? data : JSON.stringify(data)
    };

    fetch('/process', options)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text); });  // HTML 응답을 텍스트로 읽어 오류로 처리
            }
            return response.json();
        })
        .then(result => {
            if (result.image_links && result.image_ids && result.image_info) {
                displayImages(result.image_links, result.image_ids, result.image_info);
            } else {
                console.error('Invalid response format:', result);
                alert('서버에서 잘못된 형식의 응답을 받았습니다.');
            }
        })
        .catch(error => {
            alert('An error occurred: ' + error.message);
        })
        .finally(() => {
            isRequesting = false;
            hideLoadingPopup();
        });
}

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

document.querySelectorAll('.example-text').forEach(box => {
    box.addEventListener('click', function () {
        searchInput.value = this.querySelector('span').textContent.trim();
        toggleGetStartedButton();
        if (!getStartedBtn.disabled) {
            getStartedBtn.click();
        }
    });
});

// 페이지 상단으로 스크롤 기능 구현
document.getElementById('scrollToTopBtn').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

function handleFileUpload() {
    if (fileInput.files.length && !isRequesting) {
        isRequesting = true;
        showLoadingPopup();
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);
        sendPostRequest(formData, true);
    }
}

function handleGetStarted() {
    if (searchInput.value.trim() && !isRequesting) {
        isRequesting = true;
        showLoadingPopup();
        const data = { text: searchInput.value.trim() };
        sendPostRequest(data);
    }
}

function showPopup(message, popupId) {
    const popup = document.getElementById(popupId);
    popup.textContent = message;
    popup.classList.add('visible');
    setTimeout(() => {
        popup.classList.remove('visible');
    }, 1500); // Show the popup for 1.5 seconds
}

fileInput.addEventListener('change', handleFileUpload);

uploadBtn.addEventListener('click', function () {
    fileInput.click();
});

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('border-blue-600');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('border-blue-600');
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('border-blue-600');
    if (e.dataTransfer.files && e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleFileUpload();
    }
});

getStartedBtn.addEventListener('click', handleGetStarted);

searchInput.addEventListener('input', toggleGetStartedButton);

clearInputBtn.addEventListener('click', function () {
    searchInput.value = '';
    toggleGetStartedButton();
    searchInput.focus(); // Clear 후 입력 필드에 포커스 유지
});

toggleGetStartedButton();

confirmDeleteBtn.addEventListener('click', function () {
    if (imageToDelete) {
        removeImageFromCart(imageToDelete.dataset.id);
        imageToDelete.remove();
        deletePopup.style.display = 'none';
        imageToDelete = null;
    }
});

cancelDeleteBtn.addEventListener('click', function () {
    deletePopup.style.display = 'none';
    imageToDelete = null;
});

confirmAddToCartBtn.addEventListener('click', function () {
    if (imageToAdd) {
        addImageToCart(imageToAdd);
        addToCartPopup.style.display = 'none';
        imageToAdd = null;
    }
});

cancelAddToCartBtn.addEventListener('click', function () {
    addToCartPopup.style.display = 'none';
    imageToAdd = null;
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