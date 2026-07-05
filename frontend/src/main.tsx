import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { AuthProvider } from "./contexts/AuthContext";
import { HomeProvider } from "./contexts/HomeContext.tsx";
import { LikedProvider } from "./contexts/LikedContext.tsx";

// createRoot(document.getElementById("root")!).render(
//   <StrictMode>
//     <AuthProvider>
//       <HomeProvider>
//       <App />
//       </HomeProvider>
//     </AuthProvider>
//   </StrictMode>,
// );

createRoot(document.getElementById("root")!).render(
  <AuthProvider>
    <LikedProvider>
      <HomeProvider>
        <App />
      </HomeProvider>
    </LikedProvider>
  </AuthProvider>,
);
