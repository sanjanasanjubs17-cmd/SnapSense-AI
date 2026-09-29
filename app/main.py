import streamlit as st
from PIL import Image
import numpy as np
import onnxruntime as ort
import os
import time

st.set_page_config(
    page_title="SnapSense AI",
    page_icon="👁️",
    layout="wide"
)

st.title("👁️ SnapSense AI")
st.subheader("See locally. Understand instantly. Share nothing.")

st.write(
    "A privacy-first AI visual assistant designed for fast, "
    "local image understanding."
)

st.divider()

uploaded_file = st.file_uploader(
    "📷 Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Input Image",
        use_container_width=True
    )

    model_path = os.path.join(
        "models",
        "object_detection_nanodet_2022nov.onnx"
    )

    if os.path.exists(model_path):

        try:
            session = ort.InferenceSession(
                model_path,
                providers=["CPUExecutionProvider"]
            )

            img = image.resize((416, 416))

            img_array = (
                np.array(img).astype(np.float32) / 255.0
            )

            input_tensor = np.transpose(
                img_array,
                (2, 0, 1)
            )

            input_tensor = np.expand_dims(
                input_tensor,
                axis=0
            )

            input_name = session.get_inputs()[0].name

            start_time = time.time()

            outputs = session.run(
                None,
                {input_name: input_tensor}
            )

            inference_time = time.time() - start_time

            st.success(
                "🧠 Model inference completed!"
            )

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Inference Engine",
                    "ONNX Runtime"
                )

            with col2:
                st.metric(
                    "Processing Mode",
                    "Local"
                )

            with col3:
                st.metric(
                    "Inference Time",
                    f"{inference_time:.2f}s"
                )

            st.info(
                "🔒 Privacy: Image processing is performed locally. "
                "No cloud AI service is required."
            )

            st.subheader(
                "🔍 AI Vision Analysis"
            )

            st.write(
                f"Model produced {len(outputs)} output tensors."
            )

            for i, output in enumerate(outputs):

                st.write(
                    f"Output {i + 1} shape: "
                    f"`{output.shape}`"
                )

            st.subheader(
                "🧠 AI Vision Summary"
            )

            st.write(
                "The uploaded image was processed locally "
                "using an ONNX-based vision model."
            )

            st.write(
                "The model generated multiple vision feature "
                "outputs for image analysis."
            )

            col_a, col_b = st.columns(2)

            with col_a:
                st.metric(
                    "Model Outputs",
                    len(outputs)
                )

            with col_b:
                st.metric(
                    "Input Resolution",
                    "416 × 416"
                )

            st.success(
                "🔒 Privacy-first processing: "
                "No cloud AI service is required."
            )

        except Exception as e:

            st.error(
                "❌ AI inference error"
            )

            st.code(
                str(e)
            )

    else:

        st.error(
            "❌ AI model not found. "
            "Please check the models folder."
        )

else:

    st.info(
        "👆 Upload an image to begin."
    )