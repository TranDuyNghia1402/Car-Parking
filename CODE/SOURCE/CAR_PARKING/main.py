import cv2 as cv
import os
from GATE.ANPR_Support import *
from GATE.Gate import Gate

path = 'D:/Car_Parking/Images/self_cap_Data/test_Data/data/images/train'
img_name1 = 'z4614410846641_41df6b0ae930b126da71be6bdee5dbd2.jpg'
img_name2 = 'z4614410866250_950a4e951d0eb8e5602b04a3ab1fdc77.jpg'
img_name3 = 'z4614410832869_81b7bb4e8d73e1c586924d460cd35dc6.jpg'
img_name4 = 'z4614410840545_45d2180cc13bd4082cf9fc783d4b311c.jpg'
img_name5 = 'z4614410871751_35b99c2749fe0bf5eb255986d9105bf1.jpg'
img_name6 = 'z4614409464006_ad166d3f0b2cb3b6d0768e48d6233e12.jpg'


def gateIn():
    # capture = cv.VideoCapture(0)
    # isTrue, frame = capture.read()
    # gateIn = Gate(camera_frame=frame)
    # while isTrue:
    #     gateIn.plate_regconition()
    #     isTrue, frame = capture.read()
    #     cv.imshow('frame', frame)
    #     if cv.waitKey(1) & 0xFF == ord('s'):
    #         print('s')
    #         gate_in.send_command(ser, OPEN_COMMAND)
    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         print('quit')
    #         gate_in.send_command(ser, CLOSE_COMMAND)
    #         # break
    # capture.release()
    # cv.destroyAllWindows()
    image = cv.imread(os.path.join(path, img_name4))
    gate_in = Gate(image_input=image)
    is_number_plate_in, cap_in_img = gate_in.plate_regconition()
    if is_number_plate_in:
        license_text_in = get_license_plate_text(cap_in_img).replace('\n', '')
        current_time_in = get_current_time()
        if license_text_in is not None:
            qr_path, data = generate_qrcode()
            write_data_to_csv(license_text_in, data, current_time_in)
            print(qr_path)
            cv.imshow('IDENTIFIER', cv.imread(qr_path))
    read_data_from_csv()
    cv.waitKey(0)


def gateOut():
    image = cv.imread(os.path.join(path, img_name2))
    gate_out = Gate(image_input=image)
    is_number_plate_out, cap_out_img = gate_out.plate_regconition()
    if is_number_plate_out:
        license_text_out = cleanup_text(get_license_plate_text(cap_out_img))
        current_time_out = get_current_time()
        if license_text_out is not None:
            if check_data_is_correct(license_text_out, 'GHo7FvJgLWTm'):
                time_in = get_time_in(license_text_out)
                remove_data(license_text_out)
            else:
                print('Data Wrong')
    cv.waitKey(0)


def read_data():
    read_data_from_csv()


if __name__ == "__main__":
    # gateIn()
    gateOut()
    read_data()
