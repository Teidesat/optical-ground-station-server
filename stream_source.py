#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StreamSource class to handle video streaming from a camera.
"""

import threading

import cv2 as cv


class StreamSource:
    def __init__(self, video_source: int = 0):
        self.video_source = video_source

        self.vid_cap = cv.VideoCapture(self.video_source)
        if self.vid_cap is None or not self.vid_cap.isOpened():
            raise ValueError(
                f"Error: video source nº {self.video_source} is already in use."
            )

        self.foreground_buffer = None
        self.background_buffer = None

        success, frame = self.vid_cap.read()
        if not success:
            raise ValueError(
                f"Error: could not read video source nº {self.video_source}."
            )

        ret, img_encoded = cv.imencode(".jpg", frame)
        if ret:
            self.foreground_buffer = img_encoded.tobytes()

        self.stop_event = threading.Event()
        self.fill_buffer_thread = threading.Thread(target=self.fill_buffer)
        self.fill_buffer_thread.start()

    def __del__(self):
        if (
            hasattr(self, "fill_buffer_thread")
            and self.fill_buffer_thread is not None
            and self.fill_buffer_thread.is_alive()
        ):
            self.stop_event.set()
            self.fill_buffer_thread.join(timeout=1)

        if (
            hasattr(self, "cap")
            and self.vid_cap is not None
            and self.vid_cap.isOpened()
        ):
            self.vid_cap.release()

    def fill_buffer(self):
        while not self.stop_event.is_set():
            _, frame = self.vid_cap.read()
            frame = cv.flip(frame, 1)

            ret, img_encoded = cv.imencode(".jpg", frame)
            if ret:
                self.background_buffer = img_encoded.tobytes()

            self.foreground_buffer = self.background_buffer
            cv.waitKey(1)

    def get_frame(self):
        return self.foreground_buffer
