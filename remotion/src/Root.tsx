import { Composition } from "remotion";
import { Smoke } from "./Smoke";
import { Capability } from "./Capability";
export const Root: React.FC = () => (
  <>
  <Composition id="Capability" component={Capability} durationInFrames={30} fps={30} width={1080} height={1920} />
  <Composition id="Smoke" component={Smoke} durationInFrames={60} fps={30} width={1080} height={1920} />
  </>
);
