import cv2 
import math
import numpy as np
import random
def ModInv():
    """
        Form equation 1 = inv(a)*a mod m. we find inv(a)
        Inverse exist only if a and m be Coprime
    """
    for i in range(2,m):
        if (A * i) % m == 1 :
            return i
    return 1

def encryption(original_img):
    """
    Encryption of image 
    """
    height = original_img.shape[0]
    width = original_img.shape[1]
    for i in range(0,height):
        for j in range(0,width):
            a = original_img[i][j]      # rgb list
            r = (A*a[0] + B)%m
            g = (A*a[1] + B)%m
            b = (A*a[2] + B)%m
            original_img[i][j] = [r,g,b]
        
    cv2.imwrite('encrypted_img.png', original_img)  # saving encrypted image



def decryption(encrypted_img):
    height = encrypted_img.shape[0]
    width = encrypted_img.shape[1]
    inv_a = ModInv()
    for i in range(0,height):
        for j in range(0,width):
            a = encrypted_img[i][j]         # rgb list
            r = (inv_a*(a[0] - B)) % m
            g = (inv_a*(a[1] - B)) % m
            b = (inv_a*(a[2] - B)) % m
            encrypted_img[i][j] = [r,g,b]

    cv2.imwrite('decrypted_img.png', encrypted_img)   # Saving decrypted image


def createShare(original_img,n):
    height = original_img.shape[0]
    width = original_img.shape[1]
    blank_image = np.zeros((height,width,3), np.uint8)
    for share in range(0,n):
        if share < n-1 :
            for i in range(0,height):
                for j in range(0,width):
                    # a = temp_img[i][j]
                    r = random.randint(0,255)
                    g = random.randint(0,255)
                    b = random.randint(0,255)
                    blank_image[i][j] = [r,g,b]
            cv2.imwrite('random{}.png'.format(share+1),blank_image)
        if share == 0:
            cv2.imwrite('share{}.png'.format(share+1),blank_image)

        elif share > 0 and share <= n-2 :
            temp_img = cv2.imread('random{}.png'.format(share))
            for i in range(0,height):
                for j in range(0,width):
                    a = blank_image[i][j]
                    b = temp_img[i][j]
                    temp_img[i][j] = [(a[0]^b[0]), (a[1]^b[1]), (a[2]^b[2])]
            cv2.imwrite('share{}.png'.format(share+1),temp_img)

        else:
            temp_img = cv2.imread('random{}.png'.format(share))
            for i in range(0,height):
                for j in range(0,width):
                    a = temp_img[i][j]
                    b = original_img[i][j]
                    temp_img[i][j] = [(a[0]^b[0]), (a[1]^b[1]), (a[2]^b[2])]

            cv2.imwrite('share{}.png'.format(share+1), temp_img)
           
                
def combine(n):
    org_img = cv2.imread('share1.png')
    height = org_img.shape[0]
    width = org_img.shape[1]
    for share in range(2,n+1):
        temp_img = cv2.imread('share{}.png'.format(share))
        for i in range(0, height):
            for j in range(0,width):
                a = temp_img[i][j]
                b = org_img[i][j]
                org_img[i][j] = [(a[0]^b[0]), (a[1]^b[1]), (a[2]^b[2])]

    cv2.imwrite('share_org.png', org_img)

#------------------------------------------- main program
m = 256
A = 71
B = random.randint(31,255)

original_img = cv2.imread('girl.png')
encryption(original_img)
encrypted_img = cv2.imread('encrypted_img.png')
decryption(encrypted_img)
createShare(original_img,4)
combine(4)