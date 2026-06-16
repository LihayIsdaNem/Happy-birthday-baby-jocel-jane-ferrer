from __future__ import annotations

import html
import shutil
import webbrowser
from pathlib import Path
from string import Template


# =========================
# Edit these details
# =========================
CELEBRANT_NAME = "Birthday Baby"
SENDER_NAME = "Your Baby Lihay"
PAGE_TITLE = "Birthday Surprise"

MESSAGE_LINES = [
    "My Baby, you are the love of my life and the most beautiful part of my heart.",
    "Every day with you feels like a blessing, and I am so thankful that I get to love you.",
    "On your birthday, I hope you feel how deeply you are loved, cherished, and treasured by me.",
    "May your heart always be full of happiness, and may I always be one of the reasons you smile.",
]

# Optional local files. Leave blank if you do not want to use them.
# Example: PHOTO_PATH = "assets/celebrant.jpg"
# Example: MUSIC_PATH = "assets/birthday-song.mp3"
PHOTO_PATH = "assets/celebrant.jpg"
MUSIC_PATH = "assets/birthday-song.mp3"

OPEN_IN_BROWSER = True


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
ASSET_DIR = OUTPUT_DIR / "assets"
OUTPUT_FILE = OUTPUT_DIR / "index.html"


def escape_text(value: str) -> str:
    return html.escape(str(value), quote=True)


def copy_optional_asset(source: str) -> str:
    if not source:
        return ""

    source_path = Path(source)
    if not source_path.is_absolute():
        source_path = BASE_DIR / source_path

    if not source_path.exists() or not source_path.is_file():
        print(f"Optional asset not found, skipping: {source_path}")
        return ""

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    target_path = ASSET_DIR / source_path.name
    shutil.copy2(source_path, target_path)
    return f"assets/{target_path.name}"


def build_message_html() -> str:
    paragraphs = "\n".join(
        f"                <p>{escape_text(line)}</p>" for line in MESSAGE_LINES if line.strip()
    )
    return paragraphs or "                <p>Wishing you a birthday full of joy and good memories.</p>"


def build_photo_html(photo_src: str) -> str:
    if not photo_src:
        return """
            <div class="birthday-icon" aria-hidden="true">&#127874;</div>"""

    return f"""
            <figure class="photo-frame">
                <img src="{escape_text(photo_src)}" alt="{escape_text(CELEBRANT_NAME)}">
            </figure>"""


def build_music_html(music_src: str) -> str:
    audio_html = ""
    if music_src:
        audio_html = f"""
            <audio id="birthdayMusic" preload="auto" loop>
                <source src="{escape_text(music_src)}" type="audio/mpeg">
            </audio>"""

    return f"""
            <button class="ghost-button" id="musicButton" type="button">
                <span aria-hidden="true">&#9835;</span>
                <span>Play birthday music</span>
            </button>
            {audio_html}"""


def build_html() -> str:
    photo_src = copy_optional_asset(PHOTO_PATH)
    music_src = copy_optional_asset(MUSIC_PATH)

    template = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$page_title</title>
    <style>
        :root {
            --rose: #ff4f81;
            --rose-dark: #d92d63;
            --gold: #f6b93b;
            --sky: #38bdf8;
            --mint: #34d399;
            --ink: #261a2f;
            --muted: #6b5d70;
            --paper: #fffafc;
            --panel: rgba(255, 255, 255, 0.94);
        }

        * {
            box-sizing: border-box;
        }

        html {
            min-height: 100%;
        }

        body {
            margin: 0;
            min-height: 100vh;
            min-height: 100svh;
            font-family: Arial, Helvetica, sans-serif;
            color: var(--ink);
            background:
                radial-gradient(circle at 20% 20%, rgba(255, 79, 129, 0.18), transparent 28%),
                radial-gradient(circle at 80% 12%, rgba(56, 189, 248, 0.18), transparent 24%),
                linear-gradient(135deg, #fff0f5 0%, #fff9e8 45%, #ebfbff 100%);
            display: grid;
            place-items: center;
            overflow-x: hidden;
            padding: 24px;
            -webkit-text-size-adjust: 100%;
        }

        .confetti-canvas {
            position: fixed;
            inset: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 5;
        }

        .scene {
            position: relative;
            width: min(100%, 780px);
            min-height: 560px;
            display: grid;
            place-items: center;
            overflow: visible;
        }

        .balloon {
            position: fixed;
            bottom: -150px;
            width: 54px;
            height: 70px;
            border-radius: 50% 50% 46% 46%;
            opacity: 0.88;
            --float-mid-x: 18px;
            --float-end-x: -12px;
            z-index: 4;
            pointer-events: none;
            will-change: transform;
            animation: floatUp 20s linear infinite;
            box-shadow: inset -10px -12px 18px rgba(38, 26, 47, 0.12);
        }

        .balloon::before {
            content: "";
            position: absolute;
            top: 14px;
            left: 15px;
            width: 13px;
            height: 20px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.42);
            transform: rotate(24deg);
        }

        .balloon::after {
            content: "";
            position: absolute;
            left: 50%;
            bottom: -72px;
            width: 1px;
            height: 78px;
            background: rgba(38, 26, 47, 0.25);
        }

        .balloon.one {
            left: 2%;
            bottom: -140px;
            background: var(--rose);
            --float-mid-x: 22px;
            --float-end-x: -18px;
            animation-duration: 21s;
            animation-delay: -7s;
        }

        .balloon.two {
            right: 3%;
            bottom: -180px;
            background: var(--sky);
            --float-mid-x: -24px;
            --float-end-x: 16px;
            animation-duration: 24s;
            animation-delay: -15s;
        }

        .balloon.three {
            left: 10%;
            bottom: -120px;
            background: var(--gold);
            --float-mid-x: 16px;
            --float-end-x: -22px;
            animation-duration: 19s;
            animation-delay: -3s;
        }

        .balloon.four {
            right: 14%;
            bottom: -155px;
            width: 48px;
            height: 64px;
            background: #a855f7;
            --float-mid-x: -18px;
            --float-end-x: 24px;
            animation-duration: 22s;
            animation-delay: -11s;
        }

        .balloon.five {
            left: 20%;
            bottom: -135px;
            width: 42px;
            height: 56px;
            background: #fb7185;
            --float-mid-x: 14px;
            --float-end-x: -16px;
            animation-duration: 18s;
            animation-delay: -9s;
        }

        .balloon.six {
            right: 22%;
            bottom: -170px;
            width: 46px;
            height: 61px;
            background: var(--mint);
            --float-mid-x: -14px;
            --float-end-x: 18px;
            animation-duration: 23s;
            animation-delay: -5s;
        }

        .balloon.seven {
            left: -3%;
            bottom: -125px;
            width: 44px;
            height: 58px;
            background: #f97316;
            --float-mid-x: 26px;
            --float-end-x: -10px;
            animation-duration: 20s;
            animation-delay: -13s;
        }

        .balloon.eight {
            right: -2%;
            bottom: -145px;
            width: 50px;
            height: 66px;
            background: #22c55e;
            --float-mid-x: -20px;
            --float-end-x: 22px;
            animation-duration: 25s;
            animation-delay: -18s;
        }

        .balloon.nine {
            left: 28%;
            bottom: -165px;
            width: 40px;
            height: 54px;
            background: #facc15;
            --float-mid-x: 12px;
            --float-end-x: -20px;
            animation-duration: 17s;
            animation-delay: -2s;
        }

        .balloon.ten {
            left: 38%;
            bottom: -150px;
            width: 47px;
            height: 63px;
            background: #06b6d4;
            --float-mid-x: -16px;
            --float-end-x: 18px;
            animation-duration: 26s;
            animation-delay: -6s;
        }

        .balloon.eleven {
            right: 34%;
            bottom: -190px;
            width: 39px;
            height: 53px;
            background: #ec4899;
            --float-mid-x: 20px;
            --float-end-x: -14px;
            animation-duration: 18s;
            animation-delay: -14s;
        }

        .balloon.twelve {
            left: 46%;
            bottom: -130px;
            width: 52px;
            height: 69px;
            background: #84cc16;
            --float-mid-x: -22px;
            --float-end-x: 12px;
            animation-duration: 24s;
            animation-delay: -21s;
        }

        .balloon.thirteen {
            right: 45%;
            bottom: -175px;
            width: 43px;
            height: 58px;
            background: #ef4444;
            --float-mid-x: 15px;
            --float-end-x: -24px;
            animation-duration: 21s;
            animation-delay: -8s;
        }

        .balloon.fourteen {
            left: 58%;
            bottom: -145px;
            width: 41px;
            height: 55px;
            background: #14b8a6;
            --float-mid-x: -12px;
            --float-end-x: 20px;
            animation-duration: 19s;
            animation-delay: -16s;
        }

        .balloon.fifteen {
            right: 57%;
            bottom: -200px;
            width: 49px;
            height: 65px;
            background: #8b5cf6;
            --float-mid-x: 24px;
            --float-end-x: -12px;
            animation-duration: 27s;
            animation-delay: -4s;
        }

        .balloon.sixteen {
            left: 72%;
            bottom: -155px;
            width: 44px;
            height: 59px;
            background: #f59e0b;
            --float-mid-x: -18px;
            --float-end-x: 26px;
            animation-duration: 22s;
            animation-delay: -19s;
        }

        .balloon.seventeen {
            right: 72%;
            bottom: -125px;
            width: 38px;
            height: 51px;
            background: #0ea5e9;
            --float-mid-x: 13px;
            --float-end-x: -18px;
            animation-duration: 20s;
            animation-delay: -10s;
        }

        .balloon.eighteen {
            left: 86%;
            bottom: -185px;
            width: 45px;
            height: 60px;
            background: #d946ef;
            --float-mid-x: -26px;
            --float-end-x: 10px;
            animation-duration: 25s;
            animation-delay: -23s;
        }

        .card {
            width: min(100%, 520px);
            border-radius: 8px;
            background: var(--panel);
            border: 1px solid rgba(255, 255, 255, 0.75);
            box-shadow: 0 24px 70px rgba(69, 33, 77, 0.18);
            padding: 34px;
            text-align: center;
            position: relative;
            z-index: 2;
            backdrop-filter: blur(12px);
        }

        .eyebrow {
            margin: 0 0 12px;
            color: var(--rose-dark);
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
        }

        .birthday-icon {
            font-size: 64px;
            line-height: 1;
            margin-bottom: 14px;
            animation: bounce 1s ease-in-out infinite alternate;
        }

        .photo-frame {
            width: 150px;
            height: 150px;
            margin: 0 auto 18px;
            border-radius: 8px;
            overflow: hidden;
            border: 6px solid #ffffff;
            box-shadow: 0 16px 35px rgba(217, 45, 99, 0.22);
            background: #fff;
        }

        .photo-frame img {
            width: 100%;
            height: 100%;
            display: block;
            object-fit: cover;
        }

        h1 {
            margin: 0;
            color: var(--ink);
            font-size: 38px;
            line-height: 1.08;
            letter-spacing: 0;
        }

        .lead {
            margin: 16px auto 0;
            max-width: 410px;
            color: var(--muted);
            font-size: 18px;
            line-height: 1.55;
        }

        .actions {
            min-height: 78px;
            display: grid;
            place-items: center;
            margin-top: 18px;
            overflow: visible;
        }

        button {
            min-height: 48px;
            border: 0;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            transition: transform 0.22s ease, background 0.22s ease, box-shadow 0.22s ease;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }

        .gift-button {
            padding: 0 22px;
            background: var(--rose);
            color: white;
            box-shadow: 0 12px 28px rgba(217, 45, 99, 0.28);
            position: relative;
            will-change: transform;
        }

        .gift-button:hover {
            background: var(--rose-dark);
        }

        .gift-button.ready {
            background: var(--mint);
            color: #063322;
            box-shadow: 0 12px 28px rgba(52, 211, 153, 0.28);
        }

        .message {
            display: none;
            margin-top: 22px;
            border-radius: 8px;
            background: #fff7fb;
            border: 1px solid rgba(217, 45, 99, 0.14);
            padding: 22px;
            text-align: left;
            animation: reveal 0.5s ease both;
        }

        .message.is-visible {
            display: block;
        }

        .message h2 {
            margin: 0 0 12px;
            color: var(--rose-dark);
            font-size: 24px;
            letter-spacing: 0;
        }

        .message p {
            margin: 0 0 12px;
            color: #3d3344;
            font-size: 17px;
            line-height: 1.65;
        }

        .signature {
            margin-top: 18px;
            color: var(--ink);
            font-weight: 800;
        }

        .ghost-button {
            width: 100%;
            margin-top: 14px;
            background: white;
            border: 1px solid rgba(38, 26, 47, 0.14);
            color: var(--ink);
            display: inline-flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
        }

        .ghost-button:hover {
            box-shadow: 0 10px 25px rgba(38, 26, 47, 0.08);
        }

        .replay-button {
            margin-top: 16px;
            padding: 0 18px;
            background: var(--ink);
            color: white;
        }

        .surprise-button {
            width: 100%;
            margin-top: 16px;
            padding: 0 18px;
            background: var(--ink);
            color: white;
        }

        .surprise-panel {
            display: none;
            margin-top: 18px;
            padding: 16px;
            border-radius: 8px;
            background: #ffffff;
            border: 1px dashed rgba(217, 45, 99, 0.35);
            animation: reveal 0.35s ease both;
        }

        .surprise-panel.is-visible {
            display: block;
        }

        .surprise-panel p {
            margin: 0 0 12px;
            font-weight: 800;
            color: var(--rose-dark);
        }

        .option-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
        }

        .date-option {
            min-height: 46px;
            padding: 0 12px;
            background: #fff7fb;
            border: 1px solid rgba(217, 45, 99, 0.18);
            color: var(--ink);
            box-shadow: 0 8px 20px rgba(38, 26, 47, 0.06);
            will-change: transform, opacity;
        }

        .date-option:hover {
            background: #ffe6f0;
        }

        .date-option.fly-away {
            pointer-events: none;
            animation: flyAway 0.58s ease-in forwards;
        }

        .date-option.selected {
            background: var(--mint);
            color: #063322;
            border-color: rgba(6, 51, 34, 0.18);
        }

        .option-status {
            min-height: 22px;
            margin: 12px 0 0;
            color: var(--muted);
            font-size: 14px;
            text-align: center;
        }

        .footer {
            margin: 22px 0 0;
            color: var(--muted);
            font-size: 13px;
        }

        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-10px); }
        }

        @keyframes reveal {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes floatUp {
            0% {
                opacity: 0;
                transform: translate3d(0, 0, 0) rotate(-5deg);
            }
            8% {
                opacity: 0.88;
            }
            50% {
                transform: translate3d(var(--float-mid-x), calc(-50vh - 130px), 0) rotate(4deg);
            }
            92% {
                opacity: 0.88;
            }
            100% {
                opacity: 0;
                transform: translate3d(var(--float-end-x), calc(-100vh - 260px), 0) rotate(-4deg);
            }
        }

        @keyframes flyAway {
            to {
                opacity: 0;
                transform: translate(var(--fly-x, 240px), -150px) rotate(18deg) scale(0.75);
            }
        }

        @media (max-width: 640px) {
            body {
                min-height: 100svh;
                padding: 10px;
                padding-top: max(10px, env(safe-area-inset-top));
                padding-bottom: max(10px, env(safe-area-inset-bottom));
                align-items: start;
            }

            .scene {
                width: 100%;
                min-height: calc(100svh - 20px);
                padding: 8px 0;
                align-items: start;
            }

            .card {
                width: 100%;
                max-height: calc(100svh - 20px);
                overflow-y: auto;
                -webkit-overflow-scrolling: touch;
                padding: 20px 14px;
                box-shadow: 0 14px 36px rgba(69, 33, 77, 0.16);
            }

            .birthday-icon {
                font-size: 54px;
                margin-bottom: 10px;
            }

            .photo-frame {
                width: 118px;
                height: 118px;
                margin-bottom: 12px;
            }

            h1 {
                font-size: 29px;
            }

            .lead {
                font-size: 15.5px;
                line-height: 1.45;
            }

            .actions {
                min-height: 104px;
                margin-top: 10px;
            }

            button {
                min-height: 52px;
                font-size: 15px;
            }

            .gift-button {
                width: min(100%, 290px);
                padding: 0 14px;
            }

            .message {
                margin-top: 14px;
                padding: 16px;
            }

            .message h2 {
                font-size: 22px;
            }

            .message p {
                font-size: 15.5px;
                line-height: 1.55;
            }

            .surprise-panel {
                padding: 12px;
            }

            .date-option {
                min-height: 50px;
            }

            .balloon {
                width: 34px;
                height: 46px;
                opacity: 0.58;
            }

            .balloon::after {
                bottom: -48px;
                height: 54px;
            }

            .balloon.two,
            .balloon.three,
            .balloon.five,
            .balloon.six,
            .balloon.nine,
            .balloon.eleven,
            .balloon.twelve,
            .balloon.fifteen,
            .balloon.seventeen {
                display: none;
            }

            .option-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                scroll-behavior: auto !important;
                transition-duration: 0.01ms !important;
            }

            .balloon {
                animation-duration: 28s !important;
                animation-iteration-count: infinite !important;
            }
        }
    </style>
</head>
<body>
    <canvas class="confetti-canvas" id="confettiCanvas" aria-hidden="true"></canvas>

    <main class="scene">
        <div class="balloon one" aria-hidden="true"></div>
        <div class="balloon two" aria-hidden="true"></div>
        <div class="balloon three" aria-hidden="true"></div>
        <div class="balloon four" aria-hidden="true"></div>
        <div class="balloon five" aria-hidden="true"></div>
        <div class="balloon six" aria-hidden="true"></div>
        <div class="balloon seven" aria-hidden="true"></div>
        <div class="balloon eight" aria-hidden="true"></div>
        <div class="balloon nine" aria-hidden="true"></div>
        <div class="balloon ten" aria-hidden="true"></div>
        <div class="balloon eleven" aria-hidden="true"></div>
        <div class="balloon twelve" aria-hidden="true"></div>
        <div class="balloon thirteen" aria-hidden="true"></div>
        <div class="balloon fourteen" aria-hidden="true"></div>
        <div class="balloon fifteen" aria-hidden="true"></div>
        <div class="balloon sixteen" aria-hidden="true"></div>
        <div class="balloon seventeen" aria-hidden="true"></div>
        <div class="balloon eighteen" aria-hidden="true"></div>

        <section class="card" aria-live="polite">
            <p class="eyebrow">A birthday surprise</p>
            $photo_html
            <h1>Happy Birthday, $celebrant_name!</h1>
            <p class="lead">I prepared a small surprise for you. The gift button may be a little shy first.</p>

            <div class="actions">
                <button class="gift-button" id="giftButton" type="button">
                    Open your gift &#127873;
                </button>
            </div>

            <div class="message" id="message">
                <h2>Surprise! &#127881;</h2>
$message_html
                <div class="signature">
                    From,<br>
                    $sender_name
                </div>
                $music_html
                <button class="surprise-button" id="moreSurpriseButton" type="button">want more surprise baby?</button>
                <div class="surprise-panel" id="surprisePanel">
                    <p>Select only one for your birthday.</p>
                    <div class="option-grid" id="optionGrid">
                        <button class="date-option" type="button" data-option="movie">Movie date</button>
                        <button class="date-option" type="button" data-option="netflix">Netflix and chill</button>
                        <button class="date-option" type="button" data-option="mountaineering">Mountaineering</button>
                        <button class="date-option" type="button" data-option="skydiving">Skydiving</button>
                        <button class="date-option" type="button" data-option="free-diving">Free diving</button>
                    </div>
                    <div class="option-status" id="optionStatus"></div>
                </div>
            </div>

        </section>
    </main>

    <script>
        const giftButton = document.getElementById("giftButton");
        const message = document.getElementById("message");
        const moreSurpriseButton = document.getElementById("moreSurpriseButton");
        const surprisePanel = document.getElementById("surprisePanel");
        const optionStatus = document.getElementById("optionStatus");
        const optionButtons = Array.from(document.querySelectorAll(".date-option"));
        const canvas = document.getElementById("confettiCanvas");
        const ctx = canvas.getContext("2d");
        const colors = ["#ff4f81", "#38bdf8", "#f6b93b", "#34d399", "#7c3aed", "#fb7185"];
        const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        let moveCount = 0;
        const giftDodgeLimit = 20;
        let particles = [];
        let animationFrame = null;

        function resizeCanvas() {
            const ratio = window.devicePixelRatio || 1;
            canvas.width = Math.floor(window.innerWidth * ratio);
            canvas.height = Math.floor(window.innerHeight * ratio);
            canvas.style.width = window.innerWidth + "px";
            canvas.style.height = window.innerHeight + "px";
            ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
        }

        function unlockGiftButton() {
            giftButton.textContent = "Okay fine, open it";
            giftButton.classList.add("ready");
            giftButton.style.transform = "translate(0, 0)";
        }

        function clamp(value, min, max) {
            if (min > max) {
                return 0;
            }
            return Math.min(Math.max(value, min), max);
        }

        function getUnmovedButtonRect() {
            const currentTransform = giftButton.style.transform;
            giftButton.style.transform = "translate(0, 0)";
            const rect = giftButton.getBoundingClientRect();
            giftButton.style.transform = currentTransform;
            return rect;
        }

        function safeGiftOffset(rawX, rawY) {
            const rect = getUnmovedButtonRect();
            const margin = window.innerWidth <= 640 ? 12 : 18;
            const minX = margin - rect.left;
            const maxX = window.innerWidth - margin - rect.right;
            const minY = margin - rect.top;
            const maxY = window.innerHeight - margin - rect.bottom;

            return {
                x: clamp(rawX, minX, maxX),
                y: clamp(rawY, minY, maxY)
            };
        }

        function moveGiftButton() {
            if (moveCount >= giftDodgeLimit) {
                unlockGiftButton();
                return;
            }

            moveCount += 1;

            const progress = moveCount / giftDodgeLimit;
            const isSmallScreen = window.innerWidth <= 640;
            const xRange = (isSmallScreen ? 70 : 90) + Math.floor(progress * (isSmallScreen ? 150 : 260));
            const yRange = (isSmallScreen ? 35 : 45) + Math.floor(progress * (isSmallScreen ? 105 : 150));
            const xDirection = Math.random() > 0.5 ? 1 : -1;
            const yDirection = Math.random() > 0.5 ? 1 : -1;
            const rawX = xDirection * ((isSmallScreen ? 28 : 50) + Math.floor(Math.random() * xRange));
            const rawY = yDirection * ((isSmallScreen ? 18 : 25) + Math.floor(Math.random() * yRange));
            const offset = safeGiftOffset(rawX, rawY);

            giftButton.style.transform = "translate(" + offset.x + "px, " + offset.y + "px)";
            const teaseMessages = [
                "Catch me first",
                "Almost... maybe",
                "Too slow baby",
                "Try again",
                "Nope, not yet",
                "I'm still running"
            ];
            giftButton.textContent = teaseMessages[Math.floor(Math.random() * teaseMessages.length)];

            if (moveCount >= giftDodgeLimit) {
                window.setTimeout(unlockGiftButton, 260);
            }
        }

        function revealMessage() {
            message.classList.add("is-visible");
            giftButton.style.display = "none";
            startConfetti();
            playMusic();
        }

        function createParticle() {
            return {
                x: Math.random() * window.innerWidth,
                y: -20 - Math.random() * window.innerHeight * 0.35,
                size: 6 + Math.random() * 8,
                color: colors[Math.floor(Math.random() * colors.length)],
                speedY: 2 + Math.random() * 4,
                speedX: -1.5 + Math.random() * 3,
                rotation: Math.random() * 360,
                rotationSpeed: -8 + Math.random() * 16,
                life: 0,
                maxLife: 140 + Math.random() * 60
            };
        }

        function drawConfetti() {
            ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

            particles.forEach((particle) => {
                particle.x += particle.speedX;
                particle.y += particle.speedY;
                particle.rotation += particle.rotationSpeed;
                particle.life += 1;

                ctx.save();
                ctx.translate(particle.x, particle.y);
                ctx.rotate((particle.rotation * Math.PI) / 180);
                ctx.fillStyle = particle.color;
                ctx.fillRect(-particle.size / 2, -particle.size / 2, particle.size, particle.size * 0.65);
                ctx.restore();
            });

            particles = particles.filter((particle) => {
                return particle.y < window.innerHeight + 40 && particle.life < particle.maxLife;
            });

            if (particles.length > 0) {
                animationFrame = requestAnimationFrame(drawConfetti);
            } else {
                animationFrame = null;
                ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
            }
        }

        function startConfetti() {
            if (reduceMotion) {
                return;
            }

            particles = Array.from({ length: 170 }, createParticle);

            if (!animationFrame) {
                drawConfetti();
            }
        }

        giftButton.addEventListener("click", () => {
            if (moveCount < giftDodgeLimit) {
                moveGiftButton();
                return;
            }
            revealMessage();
        });

        function visibleNonNetflixOptions() {
            return optionButtons.filter((button) => {
                return button.dataset.option !== "netflix" && button.style.display !== "none";
            });
        }

        function checkOnlyNetflixRemains() {
            const netflixButton = optionButtons.find((button) => button.dataset.option === "netflix");
            if (visibleNonNetflixOptions().length === 0 && netflixButton) {
                netflixButton.classList.add("selected");
                optionStatus.textContent = "Only Netflix and chill remains. Looks like destiny.";
                startConfetti();
            }
        }

        function revealMoreSurprises() {
            surprisePanel.classList.add("is-visible");
            moreSurpriseButton.style.display = "none";
            optionStatus.textContent = "Pili ka po ng isa Baby wag ka na mahiya.";
        }

        function flyAwayOption(button) {
            const flyX = Math.random() > 0.5 ? "260px" : "-260px";
            button.style.setProperty("--fly-x", flyX);
            button.classList.add("fly-away");
            button.disabled = true;
            optionStatus.textContent = button.textContent.trim() + " ran away.";

            window.setTimeout(() => {
                button.style.display = "none";
                checkOnlyNetflixRemains();
            }, 620);
        }

        function chooseOption(button) {
            if (button.dataset.option === "netflix") {
                button.classList.add("selected");
                optionStatus.textContent = "Confirmed: Netflix and chill.";
                startConfetti();
                return;
            }

            flyAwayOption(button);
        }

        moreSurpriseButton.addEventListener("click", revealMoreSurprises);
        optionButtons.forEach((button) => {
            button.addEventListener("click", () => chooseOption(button));
        });

        const musicButton = document.getElementById("musicButton");
        const birthdayMusic = document.getElementById("birthdayMusic");
        let audioFileUnavailable = false;
        let synthContext = null;
        let synthPlaying = false;
        let synthLoopTimer = null;
        let activeSynthOscillators = [];
        const synthMelody = [
            { note: 523.25, duration: 0.22 },
            { note: 659.25, duration: 0.22 },
            { note: 783.99, duration: 0.28 },
            { note: 659.25, duration: 0.22 },
            { note: 698.46, duration: 0.22 },
            { note: 880.00, duration: 0.36 },
            { note: 783.99, duration: 0.28 },
            { note: 659.25, duration: 0.24 },
            { note: 587.33, duration: 0.22 },
            { note: 659.25, duration: 0.34 },
            { note: 783.99, duration: 0.30 },
            { note: 1046.50, duration: 0.44 }
        ];

        function setMusicLabel(text) {
            if (musicButton) {
                musicButton.querySelector("span:last-child").textContent = text;
            }
        }

        function stopSyntheticMusic() {
            synthPlaying = false;
            if (synthLoopTimer) {
                window.clearTimeout(synthLoopTimer);
                synthLoopTimer = null;
            }
            activeSynthOscillators.forEach((oscillator) => {
                try {
                    oscillator.stop();
                } catch (error) {
                }
            });
            activeSynthOscillators = [];
        }

        async function playSyntheticMusic() {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            if (!AudioContextClass) {
                setMusicLabel("Music unavailable");
                return;
            }

            if (!synthContext) {
                synthContext = new AudioContextClass();
            }
            if (synthContext.state === "suspended") {
                await synthContext.resume();
            }

            synthPlaying = true;
            setMusicLabel("Pause birthday music");

            function scheduleSynthLoop() {
                if (!synthPlaying) {
                    return;
                }

                const startTime = synthContext.currentTime + 0.04;
                let cursor = 0;
                activeSynthOscillators = [];

                synthMelody.forEach((tone, index) => {
                    const oscillator = synthContext.createOscillator();
                    const gain = synthContext.createGain();
                    const start = startTime + cursor;
                    const end = start + tone.duration;

                    oscillator.type = index % 2 === 0 ? "triangle" : "sine";
                    oscillator.frequency.setValueAtTime(tone.note, start);
                    gain.gain.setValueAtTime(0.0001, start);
                    gain.gain.exponentialRampToValueAtTime(0.15, start + 0.025);
                    gain.gain.exponentialRampToValueAtTime(0.0001, end);

                    oscillator.connect(gain);
                    gain.connect(synthContext.destination);
                    oscillator.start(start);
                    oscillator.stop(end + 0.03);
                    activeSynthOscillators.push(oscillator);

                    cursor += tone.duration;
                });

                synthLoopTimer = window.setTimeout(scheduleSynthLoop, Math.floor((cursor + 0.42) * 1000));
            }

            scheduleSynthLoop();
        }

        function pauseAllMusic() {
            if (birthdayMusic) {
                birthdayMusic.pause();
            }
            stopSyntheticMusic();
            setMusicLabel("Play birthday music");
        }

        async function playMusic() {
            if (birthdayMusic && !audioFileUnavailable) {
                try {
                    birthdayMusic.volume = 0.85;
                    stopSyntheticMusic();
                    await birthdayMusic.play();
                    setMusicLabel("Pause birthday music");
                    return;
                } catch (error) {
                    audioFileUnavailable = true;
                }
            }

            await playSyntheticMusic();
        }

        if (birthdayMusic) {
            birthdayMusic.addEventListener("error", () => {
                audioFileUnavailable = true;
            });
        }

        if (musicButton) {
            musicButton.addEventListener("click", async () => {
                const fileIsPlaying = birthdayMusic && !birthdayMusic.paused;
                if (fileIsPlaying || synthPlaying) {
                    pauseAllMusic();
                    return;
                }

                await playMusic();
            });
        }

        resizeCanvas();
        window.addEventListener("resize", resizeCanvas);
    </script>
</body>
</html>
""")

    return template.substitute(
        page_title=escape_text(PAGE_TITLE),
        celebrant_name=escape_text(CELEBRANT_NAME),
        sender_name=escape_text(SENDER_NAME),
        photo_html=build_photo_html(photo_src),
        music_html=build_music_html(music_src),
        message_html=build_message_html(),
    )


def save_html(html_code: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(html_code, encoding="utf-8")
    return OUTPUT_FILE


def open_page(file_path: Path) -> None:
    if OPEN_IN_BROWSER:
        webbrowser.open(file_path.resolve().as_uri())


def main() -> None:
    file_path = save_html(build_html())
    open_page(file_path)
    print("Birthday greeting page created successfully!")
    print("Open this file:", file_path.resolve())


if __name__ == "__main__":
    main()
