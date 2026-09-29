document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menuToggle");

    if (menuToggle) {
        menuToggle.addEventListener("click", () => {
            sidebar.classList.toggle("open");
        });
    }

    document.querySelectorAll("[data-open-modal]").forEach(btn => {
        btn.addEventListener("click", () => {
            const modal = document.getElementById(btn.dataset.openModal);
            if (modal) modal.classList.add("show");
        });
    });

    document.querySelectorAll("[data-close-modal], .modal-close").forEach(btn => {
        btn.addEventListener("click", () => {
            const modal = btn.closest(".modal");
            if (modal) modal.classList.remove("show");
        });
    });

    document.querySelectorAll(".modal").forEach(modal => {
        modal.addEventListener("click", e => {
            if (e.target === modal) modal.classList.remove("show");
        });
    });

    const previewBtn = document.getElementById("previewBtn");
    if (previewBtn && window.analysisApi) {
        previewBtn.addEventListener("click", async () => {
            const fields = {
                rainfall: document.getElementById("rainfall").value,
                area: document.getElementById("area").value,
                runoff_coefficient: document.getElementById("runoffCoefficient").value,
                diameter: document.getElementById("diameter").value,
                slope: document.getElementById("slope").value,
                roughness: document.getElementById("roughness").value
            };

            if (Object.values(fields).some(v => !v)) {
                alert("กรุณากรอกข้อมูลการวิเคราะห์ให้ครบก่อน Preview");
                return;
            }

            try {
                const response = await fetch(window.analysisApi, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(fields)
                });
                const data = await response.json();

                if (!response.ok) throw new Error(data.error || "Calculation error");

                const modal = document.getElementById("previewModal");
                const content = document.getElementById("previewContent");

                content.innerHTML = `
                    <div class="preview-result">
                        <div><small>Estimated Runoff</small><strong>${data.runoff} m³/s</strong></div>
                        <div><small>Pipe Capacity</small><strong>${data.pipe_capacity} m³/s</strong></div>
                        <div><small>Utilization</small><strong>${data.utilization}%</strong></div>
                        <div><small>Risk Level</small><strong class="risk-text ${data.risk_level.toLowerCase()}">${data.risk_level}</strong></div>
                    </div>
                `;
                modal.classList.add("show");
            } catch (error) {
                alert(error.message);
            }
        });
    }
});
