const canvas = document.getElementById('bezierCanvas');
const ctx = canvas.getContext('2d');
canvas.width = 500;
canvas.height = 500;

let controlPoints = [];
let draggingPoint = null;
let mode = 'add';
let sliderMode = true;
let animating = false;

function bezier(t, controlPoints) {
    const n = controlPoints.length - 1;
    let result = [0, 0];
    for (let i = 0; i <= n; i++) {
        const coeff = binomialCoeff(n, i) * Math.pow(1 - t, n - i) * Math.pow(t, i);
        result[0] += coeff * controlPoints[i][0];
        result[1] += coeff * controlPoints[i][1];
    }
    return result;
}

function binomialCoeff(n, k) {
    let result = 1;
    for (let i = 1; i <= k; i++) {
        result *= (n - i + 1) / i;
    }
    return result;
}

function drawCurve(t) {
    if (controlPoints.length < 2) return;
    
    ctx.beginPath();
    const start = bezier(0, controlPoints);
    ctx.moveTo(start[0], start[1]);

    const steps = 100;
    const maxT = (sliderMode || animating) ? t : 1;
    for (let i = 1; i <= steps; i++) {
        const t = (i / steps) * maxT;
        const point = bezier(t, controlPoints);
        ctx.lineTo(point[0], point[1]);
    }

    ctx.strokeStyle = 'blue';
    ctx.stroke();
}

function drawControlPoints() {
    controlPoints.forEach((point, index) => {
        ctx.beginPath();
        ctx.arc(point[0], point[1], 5, 0, 2 * Math.PI);
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.fillStyle = 'black';
        ctx.fillText(`P${index}`, point[0] + 10, point[1] - 10);
    });

    ctx.beginPath();
    ctx.moveTo(controlPoints[0][0], controlPoints[0][1]);
    for (let i = 1; i < controlPoints.length; i++) {
        ctx.lineTo(controlPoints[i][0], controlPoints[i][1]);
    }
    ctx.strokeStyle = 'gray';
    ctx.stroke();
}

function drawPointAtT(t) {
    if (controlPoints.length < 2) return;
    const point = bezier(t, controlPoints);
    ctx.beginPath();
    ctx.arc(point[0], point[1], 5, 0, 2 * Math.PI);
    ctx.fillStyle = 'green';
    ctx.fill();
}

function updateCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const t = parseFloat(document.getElementById('tSlider').value);
    drawCurve(t);
    drawControlPoints();
    drawPointAtT(t);
}

canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    if (mode === 'add') {
        controlPoints.push([x, y]);
    } else if (mode === 'move') {
        for (let i = 0; i < controlPoints.length; i++) {
            const dx = controlPoints[i][0] - x;
            const dy = controlPoints[i][1] - y;
            if (Math.sqrt(dx * dx + dy * dy) < 10) {
                draggingPoint = i;
                break;
            }
        }
    } else if (mode === 'remove') {
        for (let i = 0; i < controlPoints.length; i++) {
            const dx = controlPoints[i][0] - x;
            const dy = controlPoints[i][1] - y;
            if (Math.sqrt(dx * dx + dy * dy) < 10) {
                controlPoints.splice(i, 1);
                break;
            }
        }
    }
    updateCanvas();
});

canvas.addEventListener('mousemove', (e) => {
    if (draggingPoint !== null) {
        const rect = canvas.getBoundingClientRect();
        controlPoints[draggingPoint] = [
            e.clientX - rect.left,
            e.clientY - rect.top
        ];
        updateCanvas();
    }
});

canvas.addEventListener('mouseup', () => {
    draggingPoint = null;
});

document.querySelectorAll('input[name="mode"]').forEach((radio) => {
    radio.addEventListener('change', (e) => {
        mode = e.target.value;
    });
});

document.getElementById('sliderMode').addEventListener('change', (e) => {
    sliderMode = e.target.checked;
    updateCanvas();
});

document.getElementById('tSlider').addEventListener('input', (e) => {
    document.getElementById('tValue').textContent = e.target.value;
    updateCanvas();
});

document.getElementById('animateButton').addEventListener('click', () => {
    if (animating) return;
    animating = true;
    const slider = document.getElementById('tSlider');
    const startTime = performance.now();
    const duration = 2000; // 2 seconds

    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        slider.value = progress;
        document.getElementById('tValue').textContent = progress.toFixed(2);
        updateCanvas();

        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            animating = false;
        }
    }

    requestAnimationFrame(animate);
});

updateCanvas();