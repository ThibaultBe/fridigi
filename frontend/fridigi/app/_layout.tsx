import ConvexClientProvider from "@/providers/convex-client-provider";
import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <ConvexClientProvider>
      <Stack />
    </ConvexClientProvider>
  );
}
