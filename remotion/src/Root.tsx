import { Composition } from "remotion";
import { Capability } from "./Capability";
import { Reel, reelFrames, ReelProps } from "./Reel";
import { Smoke } from "./Smoke";

const demo: ReelProps = { scenes: [{ dur: 3, bg: { kind: "temple" }, dust: true, layers: [{ kind: "trail", shape: "circle", y: 900, r: 300, to: 1.5 }] }] };

export const Root: React.FC = () => (
  <>
    <Composition id="Reel" component={Reel as any} fps={30} width={1080} height={1920} durationInFrames={90} defaultProps={demo as any}
      calculateMetadata={({ props }) => ({ durationInFrames: Math.max(1, reelFrames(props as any, 30)) })} />
    <Composition id="Capability" component={Capability} durationInFrames={30} fps={30} width={1080} height={1920} />
    <Composition id="Smoke" component={Smoke} durationInFrames={60} fps={30} width={1080} height={1920} />
  </>
);
