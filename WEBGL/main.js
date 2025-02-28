// Include the gl-matrix library for matrix operations
const canvas = document.getElementById("webglCanvas");
const gl = canvas.getContext("webgl");

// Check if WebGL is supported
if (!gl) {
  alert("WebGL not supported, falling back to experimental-webgl.");
  gl = canvas.getContext("experimental-webgl");
}

if (!gl) {
  alert("Your browser does not support WebGL.");
}

// Vertex shader program
const vertexShaderSource = `
  attribute vec4 aPosition;
  attribute vec4 aColor;
  uniform mat4 uMatrix;
  varying vec4 vColor;

  void main() {
    gl_Position = uMatrix * aPosition;
    vColor = aColor;
  }
`;

// Fragment shader program
const fragmentShaderSource = `
  precision mediump float;
  varying vec4 vColor;

  void main() {
    gl_FragColor = vColor;
  }
`;

// Compile shader helper
function compileShader(gl, source, type) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error("Shader compile error:", gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }
  return shader;
}

// Initialize shaders
const vertexShader = compileShader(gl, vertexShaderSource, gl.VERTEX_SHADER);
const fragmentShader = compileShader(
  gl,
  fragmentShaderSource,
  gl.FRAGMENT_SHADER
);

// Create the WebGL program
const program = gl.createProgram();
gl.attachShader(program, vertexShader);
gl.attachShader(program, fragmentShader);
gl.linkProgram(program);

if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
  console.error("Program link error:", gl.getProgramInfoLog(program));
}

// Use the program
gl.useProgram(program);

// Attribute and uniform locations
const aPosition = gl.getAttribLocation(program, "aPosition");
const aColor = gl.getAttribLocation(program, "aColor");
const uMatrix = gl.getUniformLocation(program, "uMatrix");

let theme = "morning";
let objects = [];

// Define shapes (vertices and colors)
function createRectangle(x, y, width, height, r, g, b) {
  const x1 = x;
  const y1 = y;
  const x2 = x + width;
  const y2 = y + height;
  const r2 = theme === "morning" ? r - 0.2 : r;

  return {
    vertices: new Float32Array([
      x1, y1, // Vertex 1
      x2, y1, // Vertex 2
      x1, y2, // Vertex 3
      x2, y2, // vertex 4
      x2, y1, // Vertex 5
    ]),
    colors: new Float32Array([
      r2, g, b, 1, // V1 color
      r, g, b, 1, // V2 color
      r, g, b, 1, // V3 color
      r, g, b, 1, // V4 color
      r, g, b, 1, // V5 color
    ]),
  };
}



function createCircle(x, y, radius, segments, r, g, b) {
  const vertices = [x, y];
  const b2 = theme === "morning" ? 0 : 1.0;
  const colors = [r, g, b2, 1]; // Center color

  for (let i = 0; i <= segments; i++) {
    const angle = (i / segments) * Math.PI * 2;
    vertices.push(x + radius * Math.cos(angle), y + radius * Math.sin(angle));
    colors.push(r, g, b, 1);
  }

  return { vertices: new Float32Array(vertices), colors: new Float32Array(colors) };
}

function createTriangle(x, y, width, height, r, g, b) {
  const x1 = x;
  const y1 = y;
  const x2 = x1 + width;
  const y2 = y1 + height;
  const x3 = (x1 + x2) / 2;
  const r2 = theme === "morning" ? r - 0.5 : r;

  return {
    vertices: new Float32Array([
      x1, y1, // Vertex 1
      x2, y1, // Vertex 2
      x3, y2, // Vertex 3
    ]),
    colors: new Float32Array([
      r2, g, b, 1,
      r, g, b, 1,
      r, g, b, 1,
    ]),
  };
}

let sunX = -2.0; // Initial x-position of the sun
let moonX = -2.0; // Initial x-position of the moon (off-screen)

function updatePositions() {
  const speed = 0.001; // Movement speed

  if (theme === "morning") {
    sunX -= speed;
    if (sunX <= -1.2) { // Sun reaches the left edge
      theme = "night"; // Switch to night mode
      moonX = 1.0; // Reset moon position to the right edge
    }
  } else {
    moonX -= speed;
    if (moonX <= -1.2) { // Moon reaches the left edge
      theme = "morning"; // Switch to morning mode
      sunX = 0.7; // Reset sun position to the right edge
    }
  }
}

let carX = -0.6; // Initial x-position of the car
let carDirection = 1; // 1 for right, -1 for left
let isCarMoving = false; // Flag to control movement

function moveCar() {
  if (isCarMoving) {
    carX += 0.01 * carDirection; // Update car position

    // Check for boundaries
    if (carX > 1.0) {
      carX = -1.0; // Reset to left side when moving out of the right boundary
    } else if (carX < -1.0) {
      carX = 1.0; // Reset to right side when moving out of the left boundary
    }
  }

  requestAnimationFrame(moveCar); // Keep animating
}

// Add event listener for the button
document.getElementById("moveCar").addEventListener("click", () => {
  isCarMoving = !isCarMoving; // Toggle car movement
  if (isCarMoving) {
    moveCar(); // Start moving the car
  }
});


let characterX = 0.7; // Initial x-position of the character (right side of the canvas)
let moveSpeed = 0.02; // Speed of movement

// Event listener for keydown
document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowLeft") {
    characterX -= moveSpeed; // Move left
    if (characterX < -1.0) {
      characterX = 1.0; // Loop to the right when exiting the canvas
    }
  } else if (event.key === "ArrowRight") {
    characterX += moveSpeed; // Move right
    if (characterX > 1.0) {
      characterX = -1.0; // Loop to the left when exiting the canvas
    }
  }
});



// Buffer setup
function createBuffer(data) {
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
  return buffer;
}

function renderscene() {
  objects = [
    // House
    { shape: createRectangle(-0.7, -0.9, 0.5, 0.5, 0.8, 0.4, 0.2), translate: [0, 0, 0] }, // Base
    { shape: createRectangle(-0.5, -0.9, 0.1, 0.3, 1, 1, 1), translate: [0, 0, 0] }, // Door
    { shape: createTriangle(-0.9, -0.4, 0.9, 0.5, 1, 0, 0), translate: [0, 0, 0] }, // Roof

    // Ground
    { shape: createRectangle(-1, -1, 2, 0.1, 0, theme === "morning" ? 1 : 0.5, 0.0), translate: [0, 0, 0] },

    // Sun and Moon
    { shape: createCircle(sunX, 0.7, 0.15, 50, 1, 1, 0), translate: [0, 0, 0] }, // Sun
    { shape: createCircle(moonX, 0.7, 0.15, 50, 1, 1, 1), translate: [0, 0, 0] }, // Moon
    
    // Minecraft Character (dynamic position based on characterX)
    { shape: createRectangle(characterX - 0.05, -0.7, 0.1, 0.1, 0.9, 0.7, 0.5), translate: [0, 0, 0] }, // Head
    { shape: createRectangle(characterX - 0.05, -0.9, 0.1, 0.2, 0.2, 0.6, 0.8), translate: [0, 0, 0] }, // Body
    { shape: createRectangle(characterX - 0.1, -0.9, 0.05, 0.2, 0.2, 0.6, 0.8), translate: [0, 0, 0] }, // Left Arm
    { shape: createRectangle(characterX, -0.9, 0.05, 0.2, 0.2, 0.6, 0.8), translate: [0, 0, 0] }, // Right Arm
    { shape: createRectangle(characterX - 0.05, -1.0, 0.05, 0.1, 0.2, 0.6, 0.2), translate: [0, 0, 0] }, // Left Leg
    { shape: createRectangle(characterX, -1.0, 0.05, 0.1, 0.2, 0.6, 0.2), translate: [0, 0, 0] }, // Right Leg

    // Car
    { shape: createRectangle(carX, -0.8, 0.4, 0.2, 0.1, 0.1, 0.9), translate: [0, 0, 0] }, // Body
    { shape: createRectangle(carX + 0.05, -0.6, 0.3, 0.1, 0.2, 0.2, 1), translate: [0, 0, 0] }, // Roof
    { shape: createCircle(carX + 0.08, -0.85, 0.05, 50, 0, 0, 0), translate: [0, 0, 0] }, // Front Wheel
    { shape: createCircle(carX + 0.32, -0.85, 0.05, 50, 0, 0, 0), translate: [0, 0, 0] }, // Rear Wheel
  ];

  objects.forEach(obj => {
    obj.positionBuffer = createBuffer(obj.shape.vertices);
    obj.colorBuffer = createBuffer(obj.shape.colors);
  });
}


renderscene();

function drawScene() {
  gl.clearColor(theme === "morning" ? 0.5 : 0.1, theme === "morning" ? 0.8 : 0.1, theme === "morning" ? 1.0 : 0.3, 1.0); // Background color
  gl.clear(gl.COLOR_BUFFER_BIT);

  updatePositions(); // Update sun and moon positions
  renderscene(); // Recreate the scene with updated positions

  objects.forEach((obj) => {
    gl.bindBuffer(gl.ARRAY_BUFFER, obj.positionBuffer);
    gl.vertexAttribPointer(aPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(aPosition);

    gl.bindBuffer(gl.ARRAY_BUFFER, obj.colorBuffer);
    gl.vertexAttribPointer(aColor, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(aColor);

    const matrix = mat4.create();
    mat4.translate(matrix, matrix, obj.translate);
    gl.uniformMatrix4fv(uMatrix, false, matrix);

    gl.drawArrays(gl.TRIANGLE_FAN, 0, obj.shape.vertices.length / 2);
  });

  requestAnimationFrame(drawScene); // Keep animating
}

// Start rendering
drawScene();
