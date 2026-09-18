"""
generate_report.py
------------------
Generates the submitted Stereo Vision Depth Estimator project report.

The report is based on the final submitted report structure and content.
It does not modify the computer-vision pipeline.
"""

import os
import json
import math

import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle,
    ListFlowable,
    ListItem,
)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIAG = os.path.join(ROOT, "docs", "diagrams")
OUT = os.path.join(ROOT, "outputs")
REPORT_PATH = os.path.join(
    ROOT,
    "docs",
    "Stereo_Vision_Depth_Estimator_Report_Arjun_Tiwari.pdf",
)

os.makedirs(DIAG, exist_ok=True)


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

styles = getSampleStyleSheet()

styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
)

styles.add(
    ParagraphStyle(
        name="CoverSub",
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
    )
)

styles.add(
    ParagraphStyle(
        name="H1Report",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        spaceBefore=10,
        spaceAfter=8,
    )
)

styles.add(
    ParagraphStyle(
        name="H2Report",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        spaceBefore=8,
        spaceAfter=5,
    )
)

styles.add(
    ParagraphStyle(
        name="BodyReport",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        spaceAfter=6,
    )
)

styles.add(
    ParagraphStyle(
        name="SmallReport",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=11,
        spaceAfter=4,
    )
)

styles.add(
    ParagraphStyle(
        name="CaptionReport",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=10,
        alignment=TA_CENTER,
        spaceAfter=7,
    )
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

story = []


def p(text, style="BodyReport"):
    story.append(Paragraph(text, styles[style]))


def bullet_list(items):
    return ListFlowable(
        [
            ListItem(
                Paragraph(item, styles["BodyReport"]),
                leftIndent=12,
            )
            for item in items
        ],
        bulletType="bullet",
        start="circle",
    )


def add_image(path, width=15 * cm, caption=None, height=None):
    """
    Add an image while preserving a reasonable aspect ratio.
    """
    if not os.path.exists(path):
        story.append(
            Paragraph(
                f"[Missing image: {os.path.basename(path)}]",
                styles["SmallReport"],
            )
        )
        return

    if height is None:
        height = width * 0.62

    img = Image(path, width=width, height=height)
    story.append(img)

    if caption:
        story.append(
            Paragraph(
                caption,
                styles["CaptionReport"],
            )
        )


def image_path(filename):
    return os.path.join(DIAG, filename)


def output_path(filename):
    return os.path.join(OUT, filename)


# ---------------------------------------------------------------------------
# Generate the additional conceptual diagrams used by the submitted report
# ---------------------------------------------------------------------------

def generate_stereo_geometry():
    path = image_path("06_stereo_geometry.png")

    fig, ax = plt.subplots(figsize=(10, 4.2))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # Cameras
    ax.plot([1.0, 1.0], [0.8, 4.2], linewidth=3)
    ax.plot([9.0, 9.0], [0.8, 4.2], linewidth=3)

    ax.text(1.0, 0.35, "Left camera", ha="center", fontsize=10)
    ax.text(9.0, 0.35, "Right camera", ha="center", fontsize=10)

    # 3D point
    px, py = 5.0, 3.7
    ax.scatter(px, py, s=60)
    ax.text(px, py + 0.3, "3D point P", ha="center", fontsize=10)

    # Projection points
    ax.scatter(2.4, 2.5, s=35)
    ax.scatter(7.6, 2.5, s=35)

    ax.text(2.4, 2.15, "x₁", ha="center", fontsize=10)
    ax.text(7.6, 2.15, "x₂", ha="center", fontsize=10)

    # Projection rays
    ax.plot([1.0, px], [2.5, py], linewidth=1)
    ax.plot([9.0, px], [2.5, py], linewidth=1)

    # Image planes
    ax.plot([1.0, 2.4], [2.5, 2.5], linewidth=1)
    ax.plot([9.0, 7.6], [2.5, 2.5], linewidth=1)

    # Disparity
    ax.annotate(
        "",
        xy=(7.6, 1.35),
        xytext=(2.4, 1.35),
        arrowprops=dict(arrowstyle="<->", linewidth=1.2),
    )
    ax.text(
        5.0,
        1.55,
        "disparity  d = x₁ − x₂",
        ha="center",
        fontsize=10,
    )

    ax.text(
        5.0,
        0.75,
        "Depth:  Z = (f × B) / d",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )

    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return path


def generate_epipolar_geometry():
    path = image_path("07_epipolar_geometry.png")

    fig, ax = plt.subplots(figsize=(10, 4.5))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Cameras
    ax.scatter(2.0, 1.3, s=80)
    ax.scatter(8.0, 1.3, s=80)

    ax.text(2.0, 0.8, "Camera 1", ha="center", fontsize=10)
    ax.text(8.0, 0.8, "Camera 2", ha="center", fontsize=10)

    # 3D point
    px, py = 5.0, 4.5
    ax.scatter(px, py, s=65)
    ax.text(px, py + 0.3, "3D point P", ha="center", fontsize=10)

    # Rays
    ax.plot([2.0, px], [1.3, py], linewidth=1.5)
    ax.plot([8.0, px], [1.3, py], linewidth=1.5)

    # Epipolar line
    ax.plot(
        [6.8, 9.7],
        [0.5, 4.7],
        linewidth=1.8,
    )

    # Correct correspondence
    ax.scatter(8.0, 1.3, s=35)
    ax.text(
        8.6,
        2.0,
        "candidate x₂",
        fontsize=9,
    )

    ax.text(
        8.7,
        4.85,
        "epipolar line",
        fontsize=10,
    )

    ax.text(
        5.0,
        5.45,
        "Epipolar geometry",
        ha="center",
        fontsize=12,
        fontweight="bold",
    )

    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return path


def generate_inverse_disparity_depth():
    path = image_path("08_inverse_disparity_depth.png")

    f = 1100.0
    baseline = 0.2

    disparity = [d for d in range(1, 81)]
    depth = [(f * baseline) / d for d in disparity]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(disparity, depth)

    ax.set_xlabel("Disparity d (pixels)")
    ax.set_ylabel("Depth Z (relative unit)")
    ax.set_title("Figure 5. Inverse Disparity–Depth Relationship")
    ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return path


# Generate conceptual figures.
generate_stereo_geometry()
generate_epipolar_geometry()
generate_inverse_disparity_depth()


# ---------------------------------------------------------------------------
# Cover
# ---------------------------------------------------------------------------

story.append(Spacer(1, 4.5 * cm))

p("Stereo Vision Depth Estimator", "CoverTitle")

p(
    "A RANSAC-Based Epipolar Geometry Pipeline for Dense Depth Estimation",
    "CoverSub",
)

story.append(Spacer(1, 1.5 * cm))

p("Course: Computer Vision (CSE3010)", "CoverSub")
p("Prepared by : ARJUN TIWARI", "CoverSub")
p("Registration No. : 24BAI10141", "CoverSub")
p("B.Tech CSE (AI/ML), VIT Bhopal University", "CoverSub")

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 1. Introduction
# ---------------------------------------------------------------------------

p("1. Introduction", "H1Report")

p(
    "Depth estimation is the recovery of scene distance from image observations. "
    "In binocular stereo vision, two horizontally separated cameras observe the same "
    "scene. A 3D point appears at different image coordinates in the two views; this "
    "displacement, called disparity, provides the information required for depth recovery."
)

p(
    "<b>Stereo vision:</b> A technique that estimates scene depth by comparing "
    "corresponding observations from two viewpoints."
)

p(
    "<b>Disparity:</b> The difference in image position between corresponding points "
    "in the left and right views."
)

p(
    "<b>Depth map:</b> An image whose valid pixels contain estimated distances from the camera."
)

p(
    "<b>Epipolar geometry:</b> The geometric relationship between two camera views "
    "that constrains possible point correspondences."
)

p(
    "The pipeline combines calibration, SIFT feature matching, custom RANSAC estimation "
    "of the Fundamental matrix, pose recovery, stereo rectification, SGBM disparity "
    "estimation, and metric depth conversion."
)

p("2. Problem Statement", "H1Report")

p(
    "A single 2D image does not directly encode the distance of every visible point. "
    "The system therefore aims to recover dense depth from a stereo image pair while "
    "handling incorrect matches and geometric errors."
)

story.append(
    bullet_list(
        [
            "Find reliable correspondences.",
            "Reject outliers robustly.",
            "Estimate relative camera geometry.",
            "Rectify the stereo pair.",
            "Compute dense disparity.",
            "Convert disparity to depth and evaluate the result.",
        ]
    )
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 3. Objectives
# ---------------------------------------------------------------------------

p("3. Objectives", "H1Report")

story.append(
    bullet_list(
        [
            "Implement a complete two-view stereo pipeline.",
            "Demonstrate the normalized eight-point algorithm with RANSAC.",
            "Use SIFT correspondences and epipolar constraints.",
            "Generate dense disparity using SGBM.",
            "Recover depth using Z = fB/d.",
            "Validate results with automated tests and metrics.",
        ]
    )
)


# ---------------------------------------------------------------------------
# 4. Functional Requirements
# ---------------------------------------------------------------------------

p("4. Functional Requirements", "H1Report")

story.append(
    bullet_list(
        [
            "<b>Module 1 — Calibration & Projection:</b> maintain K, [R|t], projection "
            "matrices, and undistort images.",
            "<b>Module 2 — Feature Matching & Epipolar Geometry:</b> SIFT matching, "
            "custom RANSAC, Fundamental/Essential matrices, and relative pose.",
            "<b>Module 3 — Disparity & Depth:</b> rectification, SGBM disparity, and "
            "metric depth.",
            "<b>Input/Output:</b> two image paths in; depth map, diagnostics, and JSON metrics out.",
            "<b>Workflow:</b> load → match → geometry → rectify → disparity → depth → evaluate.",
        ]
    )
)


# ---------------------------------------------------------------------------
# 5. Non-Functional Requirements
# ---------------------------------------------------------------------------

p("5. Non-Functional Requirements", "H1Report")

story.append(
    bullet_list(
        [
            "<b>Performance:</b> approximately under four seconds for the stated "
            "1282×1110 pair on CPU.",
            "<b>Reliability:</b> floor the RANSAC inlier-ratio estimate before adaptive "
            "trial calculation.",
            "<b>Error handling:</b> explicit exceptions for missing/invalid/insufficient inputs.",
            "<b>Logging:</b> progress, match counts, inlier ratios, and disparity coverage.",
            "<b>Maintainability:</b> separate modules with independent tests.",
            "<b>Resource efficiency:</b> avoid redundant disparity computation.",
        ]
    )
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 6. System Architecture
# ---------------------------------------------------------------------------

p("6. System Architecture", "H1Report")

architecture = image_path("01_system_architecture.png")

add_image(
    architecture,
    width=17 * cm,
    height=6.0 * cm,
    caption="Figure 2. System Architecture",
)

p(
    "<b>1. Stereo Image Input:</b> The system takes a pair of horizontally offset "
    "stereo images as the primary input for depth estimation."
)

p(
    "<b>2. Calibration & Projection:</b> Camera parameters and projection models are "
    "used to prepare the images and establish the geometric relationship between the views."
)

p(
    "<b>3. Feature Matching & RANSAC Geometry:</b> SIFT features are detected and matched "
    "between the images, while RANSAC is used to estimate reliable epipolar geometry and "
    "reject incorrect matches."
)

p(
    "<b>4. Rectification & Disparity Estimation:</b> The stereo images are rectified so "
    "corresponding points align along the same scanlines, after which SGBM is used to "
    "generate a dense disparity map."
)

p(
    "<b>5. Depth & Evaluation:</b> The disparity map is converted into metric depth, and "
    "the resulting depth map is evaluated using quantitative metrics and visual outputs."
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 7. Process Workflow
# ---------------------------------------------------------------------------

p("7. Process Workflow", "H1Report")

workflow = image_path("02_workflow.png")

add_image(
    workflow,
    width=10.5 * cm,
    height=16.0 * cm,
    caption="Figure 1. End-to-End Stereo Depth Workflow",
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 8. Core Concepts and Definitions
# ---------------------------------------------------------------------------

p("8. Core Concepts and Definitions", "H1Report")

concepts = [
    (
        "Camera intrinsic matrix (K)",
        "Contains internal camera parameters such as focal lengths and principal point.",
    ),
    (
        "Extrinsic parameters",
        "Describe camera rotation and translation relative to a reference frame.",
    ),
    (
        "Projection matrix",
        "Maps a 3D point in homogeneous coordinates to image coordinates.",
    ),
    (
        "SIFT",
        "A scale-invariant local feature detector and descriptor used to establish image correspondences.",
    ),
    (
        "Fundamental matrix (F)",
        "A 3×3 rank-2 matrix expressing the epipolar constraint between two camera views.",
    ),
    (
        "Essential matrix (E)",
        "Encodes relative rotation and translation for calibrated views; here E = KᵀFK.",
    ),
    (
        "RANSAC",
        "A robust model estimation method that finds a model supported by a consistent subset of observations.",
    ),
    (
        "Sampson distance",
        "A first-order geometric error for measuring correspondence consistency with an epipolar model.",
    ),
    (
        "Stereo rectification",
        "Transforms stereo images so corresponding points lie on corresponding horizontal scanlines.",
    ),
    (
        "SGBM",
        "Semi-Global Block Matching, a stereo method that combines matching evidence with smoothness constraints.",
    ),
    (
        "Triangulation",
        "Recovers a 3D point from corresponding image observations and camera geometry.",
    ),
]

for title, description in concepts:
    p(f"<b>{title}:</b> {description}")

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 9. Stereo Geometry Visual Aid
# ---------------------------------------------------------------------------

p("9. Stereo Geometry Visual Aid", "H1Report")

add_image(
    image_path("06_stereo_geometry.png"),
    width=17 * cm,
    height=7.0 * cm,
    caption="Figure 3. Stereo Disparity Concept",
)

p(
    "In a rectified stereo setup, the same 3D point appears at different horizontal "
    "positions in the left and right images."
)

p(
    "These corresponding image positions are represented by x1 and x2, respectively."
)

p(
    "The difference between these positions is called disparity, which is given by "
    "d = x1 − x2."
)

p(
    "Disparity provides an important cue for determining how far an object is from the cameras."
)

p(
    "A larger disparity tells that the object is closer, whereas a smaller disparity "
    "indicates greater depth."
)

p(
    "The system converts disparity into metric depth using the formula Z = (f × B) / d, "
    "where f is the focal length and B is the camera baseline."
)

p(
    "<b>For a rectified stereo setup disparity and depth always follow an inverse "
    "relationship: larger disparity corresponds to smaller depth.</b>"
)

p(
    "In which the implementation uses Z = (f × B) / d."
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 10. Epipolar Geometry Visual Aid
# ---------------------------------------------------------------------------

p("10. Epipolar Geometry Visual Aid", "H1Report")

add_image(
    image_path("07_epipolar_geometry.png"),
    width=17 * cm,
    height=7.0 * cm,
    caption="Figure 4. Epipolar Geometry",
)

p(
    "Epipolar geometry describes the geometric relationship between two camera views "
    "observing the same 3D point."
)

p(
    "When a point is observed in one image, its corresponding point in the second image "
    "is constrained to lie along a specific epipolar line."
)

p(
    "This constraint significantly reduces the search area for finding corresponding points "
    "between the two images."
)

p(
    "A point in one image induces an epipolar line in the other image. Correct correspondences "
    "should satisfy the associated geometric constraint."
)

p(
    "In the diagram, the 3D point is projected onto both cameras, establishing the corresponding "
    "image observations."
)

p(
    "RANSAC helps identify reliable correspondences and reject incorrect matches before "
    "estimating the Fundamental matrix."
)

p(
    "The resulting epipolar geometry is then used to support stereo rectification and "
    "accurate disparity-based depth estimation."
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 11. Algorithm Design
# ---------------------------------------------------------------------------

p("11. Algorithm Design", "H1Report")

p("11.1 Feature Detection and Matching", "H2Report")

story.append(
    bullet_list(
        [
            "Detect SIFT keypoints.",
            "Compute descriptors.",
            "Match descriptors between views.",
            "Apply the ratio test.",
            "Send surviving point pairs to geometric estimation.",
        ]
    )
)

p("11.2 Fundamental Matrix with RANSAC", "H2Report")

story.append(
    bullet_list(
        [
            "Sample eight correspondences.",
            "Normalize coordinates.",
            "Solve the linear system with SVD.",
            "Enforce rank-2 by zeroing the smallest singular value.",
            "Score correspondences using Sampson distance.",
            "Keep the strongest inlier set.",
            "Adapt the remaining trial count using the RANSAC formula.",
        ]
    )
)

p(
    "<b>N = log(1 − p) / log(1 − wˢ)</b>",
)

p("11.3 Pose Recovery and Rectification", "H2Report")

p(
    "The Essential matrix is obtained from E = KᵀFK. Relative rotation and translation "
    "are recovered, then the stereo pair is rectified so matching becomes primarily a "
    "row-wise search."
)

p("11.4 Dense Disparity and Depth", "H2Report")

p(
    "SGBM estimates dense disparity over the rectified images. Valid disparity is converted "
    "to depth using:"
)

p("<b>Z = (f × B) / d</b>")

add_image(
    image_path("08_inverse_disparity_depth.png"),
    width=15.5 * cm,
    height=7.5 * cm,
    caption="Figure 5. Inverse Disparity–Depth Relationship",
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 12. Component Design
# ---------------------------------------------------------------------------

p("12. Component Design", "H1Report")

component_data = [
    ["Component", "Responsibility", "Output"],
    ["config.py", "Parameters and camera settings", "Configuration"],
    ["calibration.py", "Undistortion and camera geometry", "Calibration data"],
    ["epipolar.py", "SIFT, matching, RANSAC, F/E, pose", "Geometry"],
    ["depth.py", "Rectification, SGBM, depth conversion", "Disparity + depth"],
    ["evaluate.py", "Validation and metrics", "JSON metrics"],
    ["visualize.py", "Plots and overlays", "Visual diagnostics"],
    ["utils.py", "Shared utilities and I/O", "Helpers"],
    ["main.py", "Pipeline orchestration", "End-to-end run"],
]

table = Table(
    component_data,
    colWidths=[3.2 * cm, 8.0 * cm, 4.0 * cm],
)

table.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEEEEE")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.2),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
)

story.append(table)

p("13. Design Decisions and Rationale", "H1Report")

story.append(
    bullet_list(
        [
            "Custom RANSAC exposes the normalized eight-point and Sampson-distance steps.",
            "SIFT was selected for stable correspondences on the textured benchmark scene.",
            "SGBM was selected for smoother and more complete disparity than simple block matching.",
            "The modular layout supports independent testing and maintenance.",
            "Simulated intrinsics are used when physical checkerboard calibration is unavailable.",
        ]
    )
)

p("14. Dataset Description", "H1Report")

p(
    "The reference implementation was validated on the Middlebury 'Aloe' stereo pair at "
    "1282×1110 resolution. It is a textured potted-plant scene suitable for demonstrating "
    "disparity and depth separation. The pipeline accepts other horizontally offset stereo "
    "pairs through left/right image inputs."
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 15. Visual Results
# ---------------------------------------------------------------------------

p("15. Visual Results", "H1Report")

# Selected reported-results chart
fig, ax = plt.subplots(figsize=(8.5, 4.2))

labels = [
    "Feature\nmatches",
    "RANSAC\ninliers",
    "Valid\ncoverage (%)",
]
values = [1327, 999, 79.2]

bars = ax.bar(labels, values)

ax.set_ylabel("Value")
ax.set_title("Figure 6. Selected Reported Results")

for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + max(values) * 0.02,
        str(value),
        ha="center",
        va="bottom",
        fontsize=9,
    )

fig.tight_layout()

selected_chart = image_path("09_selected_reported_results.png")
fig.savefig(selected_chart, dpi=180, bbox_inches="tight")
plt.close(fig)

add_image(
    selected_chart,
    width=15.5 * cm,
    height=7.0 * cm,
)

add_image(
    architecture,
    width=17 * cm,
    height=5.2 * cm,
    caption="Stereo Vision Depth Estimation Pipeline",
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# Visual results — feature matching
# ---------------------------------------------------------------------------

add_image(
    output_path("02_feature_matches.png"),
    width=15.5 * cm,
    height=7.0 * cm,
    caption="SIFT feature matches before RANSAC filtering",
)

add_image(
    output_path("03_ransac_inlier_matches.png"),
    width=15.5 * cm,
    height=7.0 * cm,
    caption="RANSAC inlier matches (outliers rejected)",
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# Visual results — epipolar and rectified
# ---------------------------------------------------------------------------

add_image(
    output_path("04_epipolar_lines.png"),
    width=15.5 * cm,
    height=7.0 * cm,
    caption="Epipolar line overlay on the right image",
)

add_image(
    output_path("05_rectified_pair.png"),
    width=15.5 * cm,
    height=6.2 * cm,
    caption="Stereo-rectified pair",
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# Visual results — disparity and depth
# ---------------------------------------------------------------------------

add_image(
    output_path("06_disparity_map.png"),
    width=15.5 * cm,
    height=7.0 * cm,
    caption="Embedded visual output from the reference report",
)

add_image(
    output_path("07_depth_map.png"),
    width=15.5 * cm,
    height=7.0 * cm,
    caption="Embedded visual output from the reference report",
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 16. Quantitative Results
# ---------------------------------------------------------------------------

p("16. Quantitative Results", "H1Report")

# These values reproduce the submitted report.
# They are deliberately kept separate from the current pipeline's JSON output
# because the submitted report contains these exact reported measurements.

reported_metrics = [
    ["Metric", "Reported value"],
    ["Feature matches after ratio test", "1327"],
    ["RANSAC inliers", "999"],
    ["Reported RANSAC inlier ratio", "99.8%"],
    ["Fundamental matrix rank", "2"],
    ["Mean epipolar residual", "0.1352"],
    ["Disparity valid coverage", "79.2%"],
    ["Depth valid pixels", "79.2%"],
    ["Mean estimated depth", "3.466 m"],
    ["Pipeline runtime", "3.64 s"],
]

metrics_table = Table(
    reported_metrics,
    colWidths=[10.5 * cm, 5.0 * cm],
)

metrics_table.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEEEEE")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
)

story.append(metrics_table)

p(
    "The values above reproduce the measurements stated in the supplied reference report."
)


# ---------------------------------------------------------------------------
# 17. Testing Approach
# ---------------------------------------------------------------------------

p("17. Testing Approach", "H1Report")

p(
    "The reference report describes nine automated pytest tests covering calibration shapes, "
    "matching validity, Fundamental-matrix rank, RANSAC inlier ratio, epipolar residual, "
    "disparity coverage, disparity-depth behavior, NaN handling, and missing-file errors. "
    "It reports that all nine tests pass."
)


# ---------------------------------------------------------------------------
# 18. Challenges Faced
# ---------------------------------------------------------------------------

p("18. Challenges Faced", "H1Report")

story.append(
    bullet_list(
        [
            "Adaptive RANSAC trial scheduling could collapse after an unlucky early sample; "
            "a floor was added to the inlier-ratio estimate.",
            "SGBM parameters require balancing coverage and noisy matches.",
            "Invalid disparity regions must be handled consistently through the depth map "
            "and visualization.",
        ]
    )
)


# ---------------------------------------------------------------------------
# 19. Learnings and Key Takeaways
# ---------------------------------------------------------------------------

p("19. Learnings and Key Takeaways", "H1Report")

story.append(
    bullet_list(
        [
            "Rank-2 enforcement and Sampson distance improve the robustness of "
            "Fundamental-matrix estimation.",
            "Numerical-stability bugs can silently degrade a model, making automated tests important.",
            "Rectification quality strongly affects downstream disparity quality.",
            "Modular design makes the pipeline easier to understand, test, and extend.",
        ]
    )
)

story.append(PageBreak())


# ---------------------------------------------------------------------------
# 20. Future Enhancements
# ---------------------------------------------------------------------------

p("20. Future Enhancements", "H1Report")

story.append(
    bullet_list(
        [
            "Use real checkerboard-based camera calibration.",
            "Add a Streamlit interface for parameter tuning.",
            "Extend toward multi-view Structure-from-Motion and sparse 3D visualization.",
            "Investigate GPU acceleration or learned stereo matching for real-time video depth.",
        ]
    )
)


# ---------------------------------------------------------------------------
# 21. References
# ---------------------------------------------------------------------------

p("21. References", "H1Report")

story.append(
    bullet_list(
        [
            "R. Hartley and A. Zisserman, <i>Multiple View Geometry in Computer Vision</i>, Cambridge University Press.",
            "M. A. Fischler and R. C. Bolles, “Random Sample Consensus: A Paradigm for Model Fitting "
            "with Applications to Image Analysis and Automated Cartography,” <i>Communications of the ACM</i>, 1981.",
            "D. Scharstein and R. Szeliski, Middlebury Stereo Vision Datasets.",
            "OpenCV documentation — Camera Calibration and 3D Reconstruction module.",
        ]
    )
)


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

def add_footer(canvas, doc):
    canvas.saveState()

    canvas.setFont("Helvetica", 7)

    canvas.drawCentredString(
        A4[0] / 2,
        0.7 * cm,
        "Stereo Vision Depth Estimator — Project Report",
    )

    canvas.restoreState()


# ---------------------------------------------------------------------------
# Build PDF
# ---------------------------------------------------------------------------

doc = SimpleDocTemplate(
    REPORT_PATH,
    pagesize=A4,
    topMargin=1.5 * cm,
    bottomMargin=1.5 * cm,
    leftMargin=1.8 * cm,
    rightMargin=1.8 * cm,
)

doc.build(
    story,
    onFirstPage=add_footer,
    onLaterPages=add_footer,
)

print("Report written to:")
print(REPORT_PATH)