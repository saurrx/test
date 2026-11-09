import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
export const Smoke: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 12 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: "linear-gradient(#1a1030,#05030a)", justifyContent: "center", alignItems: "center" }}>
      <div style={{ color: "white", fontSize: 120, fontWeight: 800, fontFamily: "sans-serif", textAlign: "center", opacity, transform: `scale(${0.6 + 0.4 * s})` }}>
        Remotion<br />smoke test
      </div>
    </AbsoluteFill>
  );
};
