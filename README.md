# Yoga-Pose-Corrector
AI-powered yoga assistant with real-time pose analysis, audio feedback, and interactive AI chat. Uses Flask, Mediapipe, and poses_data.json for accurate form correction. Generates heatmaps for detailed insights. Enhances yoga practice with intelligent, hands-free guidance and conversational AI support.
# YogaCorrector: AI-Powered Yoga Pose Analysis

![YogaCorrector Logo](static/img/logo.png)

## Overview

YogaCorrector is an innovative AI-powered application designed to enhance your yoga practice by providing real-time feedback on your pose alignment. Leveraging advanced computer vision and machine learning techniques, this system helps users achieve correct form, prevent injuries, and deepen their understanding of various yoga asanas.

## Features

*   **Real-time Pose Analysis:** Utilizes Mediapipe for accurate and real-time detection of key body landmarks during your yoga practice.
*   **Intelligent Form Correction:** Compares your live pose against a comprehensive database of correct yoga pose configurations (`poses_data.json`).
*   **Audio Feedback:** Provides hands-free, spoken instructions to guide you on specific body parts needing adjustment, powered by `pyttsx3`.
*   **Interactive AI Chat:** Integrated with `ollama` to offer a conversational AI assistant for answering yoga-related questions and providing additional guidance.
*   **Visual Heatmaps:** Generate detailed heatmaps (`heatmap.py`) to visually represent areas of your body where angles deviate most from the ideal pose, aiding in targeted improvement.
*   **User-Friendly Interface:** A clean and intuitive web interface built with Flask, HTML, CSS, and Bootstrap for a seamless user experience.
*   **Webcam Integration:** Easily connects to your webcam for live video feed analysis.

## How it Works

1.  **Pose Selection:** Choose the yoga pose you wish to practice from a predefined list.
2.  **Live Video Feed:** Your webcam captures your movements in real-time.
3.  **Pose Estimation:** Mediapipe processes the video feed to identify 32 key body landmarks.
4.  **Angle Calculation & Comparison:** The system calculates angles between specific joints and compares them to the ideal angles stored in our `poses_data.json` database for the selected pose.
5.  **Real-time Feedback:**
    *   **Visual:** Landmarks are drawn on your video feed, with color indicators for correct/incorrect alignment.
    *   **Audio:** If deviations are detected, the system provides spoken cues (e.g., "Correct your left elbow and right knee").
6.  **Completion Status:** The application tracks your progress and indicates when you have successfully achieved the pose.
7.  **Heatmap Generation (Optional):** Upon request, a heatmap can be generated to visualize the angular differences across various body parts, offering a detailed post-practice analysis.
8.  **AI Chat:** Engage with the AI assistant for any queries or additional support during your session.

## Installation and Setup

To get YogaCorrector up and running on your local machine, follow these steps:

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)
*   Webcam

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YogaCorrector.git
cd YogaCorrector
