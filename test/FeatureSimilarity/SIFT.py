import cv2
import matplotlib.pyplot as plt

def find_and_draw_matches(img1_path, img2_path, result_path):
    # 이미지를 그레이스케일로 읽어오기
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    # SIFT 특징 검출기 생성
    sift = cv2.SIFT_create()

    # 특징점과 디스크립터 검출
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # 특징 매칭기 생성 (BFMatcher)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # 매칭 수행
    matches = bf.match(des1, des2)

    # 매칭 결과를 거리 순으로 정렬
    matches = sorted(matches, key=lambda x: x.distance)

    # 매칭 결과를 이미지로 그리기
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # 매칭 결과 이미지 출력
    plt.figure(figsize=(12, 6))
    plt.imshow(img_matches)
    plt.title('Feature Matching')
    plt.axis('off')
    plt.show()

    cv2.imwrite(result_path, img_matches)

def replace_single_backslash(input_string):
    corrected_string = ""
    i = 0
    while i < len(input_string):
        if input_string[i] == "\\":
            # Check if it's a single backslash
            if i + 1 < len(input_string) and input_string[i + 1] == "\\":
                corrected_string += "\\\\"
                i += 2
            else:
                corrected_string += "\\\\"
                i += 1
        else:
            corrected_string += input_string[i]
            i += 1
    return corrected_string

if __name__ == '__main__':
    # 이미지 경로
    img1_path = 'test\FeatureSimilarity\images\BaekYaHaeng.jpg'
    img2_path = 'test\FeatureSimilarity\images\Lady-of-Sun.jpg'
    result_path = './test/FeatureSimilarity/results/SIFT.png'

    img1_path, img2_path, result_path = replace_single_backslash(img1_path), replace_single_backslash(img2_path), replace_single_backslash(result_path)

    # 매칭 결과 표시
    find_and_draw_matches(img1_path, img2_path, result_path)