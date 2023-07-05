import cv2
import mediapipe as mp


class HandTracker():

    def __init__(self, mode=False, max_hands=2, detection_con=0.5, model_complexity=1, track_con=0.5):
        
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.model_complexity = model_complexity
        self.track_con = track_con
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complexity, self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils


    def hand_finder(self, image, draw=True):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for lm in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(image, lm, self.mp_hands.HAND_CONNECTIONS)
        
        return image


    def position_finder(self, image, hand_no=0, draw=True):
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                
                if id == 0 and draw:
                    cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                

    def finger_down(self, fingers=[]):
        """
        Returns True if fingers are down relative to the palm [0]
        """
        heights = []
        for finger in fingers:
            if finger == 4:
                heights.append(True if abs(self.lm_list[finger][2] - self.lm_list[0][2]) < 100 else False)
            else:
                heights.append(True if abs(self.lm_list[finger][2] - self.lm_list[0][2]) < 90 else False)
            #print(abs(self.lm_list[finger][2] - self.lm_list[0][2]))

        return heights
    

    def gesture_command(self):
        """
        Gets the command from the position of tips relative to 0.
        Relate to README file for command ilustration.
        """
        if self.lm_list:
            # check if forward command
            if abs(self.lm_list[8][2] - self.lm_list[0][2]) >= 150:
                h = self.finger_down(fingers=[20, 16, 12, 4])
                if len(set(h)) == 1 and h[0] == True:
                    print("forward") # TODO send data
            # check if backward command
            elif len(set(self.finger_down(fingers=[4, 12, 16, 20]))) == 1 and self.finger_down(fingers=[4, 12, 16, 20])[0] == True:
                print("backward") # TODO send data
            # check if turn left command
            elif abs(self.lm_list[20][2] - self.lm_list[0][2]) >= 135:
                h = self.finger_down(fingers=[8, 16, 12, 4])
                if len(set(h)) == 1 and h[0] == True:  
                    print("left") # TODO send data
            # check if turn right command
            elif abs(self.lm_list[4][2] - self.lm_list[0][2]) >= 80:
                h = self.finger_down(fingers=[8, 16, 12, 20])
                if len(set(h)) == 1 and h[0] == True:  
                    print("right") # TODO send data


def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    while True:
        _, image = cap.read()
        image = tracker.hand_finder(image)
        tracker.position_finder(image)
        tracker.gesture_command()
        cv2.imshow("Video", image)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()