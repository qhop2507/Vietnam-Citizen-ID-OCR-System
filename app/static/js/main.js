// ===============================
// DOM
// ===============================

const imageInput = document.getElementById("imageInput");

const inputImage = document.getElementById("inputImage");

const cardImage = document.getElementById("cardImage");

const faceImage = document.getElementById("faceImage");

const detectBtn = document.getElementById("detectBtn");

const clearBtn = document.getElementById("clearBtn");

const loading = document.getElementById("loading");

// ===============================
// Preview image
// ===============================

imageInput.addEventListener("change", function () {

    if (this.files.length === 0)
        return;

    const file = this.files[0];

    inputImage.src = URL.createObjectURL(file);

});

// ===============================
// OCR
// ===============================

detectBtn.addEventListener("click", async function () {

    if (imageInput.files.length === 0) {

        alert("Vui lòng chọn ảnh.");

        return;

    }

    loading.style.display = "block";

    detectBtn.disabled = true;

    const formData = new FormData();

    formData.append(
        "image",
        imageInput.files[0]
    );

    try {

        const response = await fetch("/ocr", {

            method: "POST",

            body: formData

        });

        const result = await response.json();

        loading.style.display = "none";

        detectBtn.disabled = false;

        if (!result.success) {

            alert("OCR thất bại.");

            return;

        }

        // =========================
        // Images
        // =========================

        if (result.card_image)
            cardImage.src =
                result.card_image + "?t=" + new Date().getTime();

        if (result.face_image)
            faceImage.src =
                result.face_image + "?t=" + new Date().getTime();

        // =========================
        // OCR Result
        // =========================

        document.getElementById("id").innerText =
            result.data.id || "";

        document.getElementById("name").innerText =
            result.data.name || "";

        document.getElementById("dob").innerText =
            result.data.dob || "";

        document.getElementById("gender").innerText =
            result.data.gender || "";

        document.getElementById("nationality").innerText =
            result.data.nationality || "";

        document.getElementById("origin_place").innerText =
            result.data.origin_place || "";

        document.getElementById("current_place").innerText =
            result.data.current_place || "";

        document.getElementById("expire_date").innerText =
            result.data.expire_date || "";

    }

    catch (err) {

        loading.style.display = "none";

        detectBtn.disabled = false;

        console.error(err);

        alert("Không thể kết nối tới API.");

    }

});

// ===============================
// Clear
// ===============================

clearBtn.addEventListener("click", function () {

    imageInput.value = "";

    inputImage.src = "/static/images/no-image.png";

    cardImage.src = "/static/images/no-image.png";

    faceImage.src = "/static/images/no-face.png";

    const ids = [

        "id",

        "name",

        "dob",

        "gender",

        "nationality",

        "origin_place",

        "current_place",

        "expire_date",

    ];

    ids.forEach(id => {

        document.getElementById(id).innerText = "";

    });

});