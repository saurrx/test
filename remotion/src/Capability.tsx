import { AbsoluteFill, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/NotoSansDevanagari";
import { useEffect, useRef, useState } from "react";

const { fontFamily } = loadFont("normal", { weights: ["700"], subsets: ["devanagari", "latin"] });

// Capability test: Devanagari shaping + a WebGL fragment shader, in one frame.
export const Capability: React.FC = () => {
  const frame = useCurrentFrame();
  const ref = useRef<HTMLCanvasElement>(null);
  const [info, setInfo] = useState("pending");
  useEffect(() => {
    const gl = ref.current?.getContext("webgl", { preserveDrawingBuffer: true });
    if (!gl) { setInfo("NO WEBGL"); return; }
    const dbg = gl.getExtension("WEBGL_debug_renderer_info");
    setInfo("webgl: " + (dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : "ok"));
    const sh = (t: number, src: string) => { const s = gl.createShader(t)!; gl.shaderSource(s, src); gl.compileShader(s); return s; };
    const p = gl.createProgram()!;
    gl.attachShader(p, sh(gl.VERTEX_SHADER, "attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}"));
    gl.attachShader(p, sh(gl.FRAGMENT_SHADER,
      "precision highp float;uniform float t;uniform vec2 r;void main(){vec2 u=(gl_FragCoord.xy-.5*r)/r.y;float d=length(u);" +
      "float g=0.02/abs(d-0.3-0.05*sin(t*3.+atan(u.y,u.x)*6.));gl_FragColor=vec4(g*vec3(1.,.7,.2)+vec3(.03,.01,.05),1.);}"));
    gl.linkProgram(p); gl.useProgram(p);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const a = gl.getAttribLocation(p, "a"); gl.enableVertexAttribArray(a); gl.vertexAttribPointer(a, 2, gl.FLOAT, false, 0, 0);
    gl.uniform1f(gl.getUniformLocation(p, "t"), frame / 30);
    gl.uniform2f(gl.getUniformLocation(p, "r"), 1080, 1920);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }, [frame]);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <canvas ref={ref} width={1080} height={1920} />
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 380 }}>
        <div style={{ fontFamily, fontSize: 84, color: "#fff", textAlign: "center", lineHeight: 1.35 }}>
          आरती का सही तरीक़ा<br />श्री राम · ॐ नमः शिवाय
        </div>
        <div style={{ fontFamily: "monospace", fontSize: 26, color: "#8f8", marginTop: 30, maxWidth: 1000, textAlign: "center" }}>{info}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
