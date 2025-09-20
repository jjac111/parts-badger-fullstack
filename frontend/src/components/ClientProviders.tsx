"use client";
import { ReactNode, useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { CssBaseline, ThemeProvider, createTheme, Snackbar, Alert } from "@mui/material";
import { useToastStore } from "@/store/toast";

export default function ClientProviders({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const theme = createTheme({ palette: { mode: "light" } });
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
      <Toaster />
    </ThemeProvider>
  );
}

function Toaster() {
  const { open, message, kind, hide } = useToastStore();
  return (
    <Snackbar open={open} autoHideDuration={3000} onClose={hide} anchorOrigin={{ vertical: "bottom", horizontal: "center" }}>
      <Alert onClose={hide} severity={kind} variant="filled" sx={{ width: "100%" }}>
        {message}
      </Alert>
    </Snackbar>
  );
}
