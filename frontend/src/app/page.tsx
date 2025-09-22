"use client";
import { useEffect, useRef, useState } from "react";
import type React from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { useUploadStore } from "@/store/upload";
import {
  Container,
  Stack,
  Typography,
  Alert,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Pagination,
  Button,
  TextField,
  LinearProgress,
} from "@mui/material";
import { useToastStore } from "@/store/toast";

type CsvResult = {
  stock_code: string;
  number_quotes_found: number;
  total_price: number;
  created_at: string;
};

export default function Home() {
  const queryClient = useQueryClient();
  const { taskId, setTaskId } = useUploadStore();
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [page, setPage] = useState(1);
  const [isUploading, setIsUploading] = useState(false);
  const [completedNotified, setCompletedNotified] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const clearTaskTimerRef = useRef<number | null>(null);

  useEffect(() => {
    const id = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(id);
  }, [search]);

  const { data: results, isLoading: isResultsLoading } = useQuery<{
    count: number;
    next: string | null;
    previous: string | null;
    results: CsvResult[];
  }>({
    queryKey: ["results", { search: debouncedSearch, page }],
    queryFn: () => api.listResults({ search: debouncedSearch, page }),
  });

  type TaskStatus = { task_id: string; state: string; info: Record<string, unknown> | string | null };
  const { data: status } = useQuery<TaskStatus>({
    queryKey: ["task", taskId],
    queryFn: () => api.taskStatus(taskId!),
    enabled: Boolean(taskId),
    refetchInterval: 1500,
    refetchIntervalInBackground: true,
    refetchOnWindowFocus: false,
    retry: 3,
  });

  const toast = useToastStore();
  const onUpload = async (selectedFile: File) => {
    try {
      setIsUploading(true);
      const res = await api.uploadCsv(selectedFile);
      setTaskId(res.task_id);
      toast.show("Upload started", "success");
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : "Upload failed";
      toast.show(message, "error");
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileSelected = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;
    setCompletedNotified(false);
    if (clearTaskTimerRef.current) {
      clearTimeout(clearTaskTimerRef.current);
      clearTaskTimerRef.current = null;
    }
    await onUpload(selected);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  useEffect(() => {
    if (!status?.state || completedNotified) return;
    if (status.state === "SUCCESS") {
      setCompletedNotified(true);
      queryClient.invalidateQueries({ queryKey: ["results"] });
      toast.show("Processing complete", "success");
      if (clearTaskTimerRef.current) clearTimeout(clearTaskTimerRef.current);
      clearTaskTimerRef.current = window.setTimeout(() => {
        setTaskId(null);
        clearTaskTimerRef.current = null;
      }, 2000);
    } else if (status.state === "FAILURE") {
      setCompletedNotified(true);
      const errorMsg = (() => {
        if (typeof status.info === "string") return status.info;
        if (status.info && typeof status.info === "object") {
          const maybeError = (status.info as { error?: unknown }).error;
          if (typeof maybeError === "string") return maybeError;
        }
        return "Processing failed";
      })();
      toast.show(errorMsg, "error");
      if (clearTaskTimerRef.current) clearTimeout(clearTaskTimerRef.current);
      clearTaskTimerRef.current = window.setTimeout(() => {
        setTaskId(null);
        clearTaskTimerRef.current = null;
      }, 2000);
    }
  }, [status?.state, completedNotified, queryClient, toast, setTaskId, status?.info]);

  useEffect(() => {
    return () => {
      if (clearTaskTimerRef.current) clearTimeout(clearTaskTimerRef.current);
    };
  }, []);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Stack spacing={3}>
        <Stack spacing={0.5}>
          <Typography variant="h4">CSV Analyzer</Typography>
          <Typography variant="body2" color="text.secondary">
            Upload a CSV to aggregate quotes by stock code.
          </Typography>
        </Stack>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} alignItems="center">
          <input ref={fileInputRef} hidden type="file" accept=".csv,text/csv" onChange={handleFileSelected} />
          <Button variant="contained" disableElevation onClick={() => fileInputRef.current?.click()} disabled={isUploading}>
            {isUploading ? "Uploading..." : "Upload CSV"}
          </Button>
          <Typography variant="body2" color="text.secondary">
            .csv files only
          </Typography>
        </Stack>

        {taskId && (
          <Alert severity={status?.state === "SUCCESS" ? "success" : status?.state === "FAILURE" ? "error" : "info"}>
            Task {taskId} — {status?.state === "SUCCESS" ? "COMPLETED" : status?.state || "PENDING"}
          </Alert>
        )}

        <Paper sx={{ p: 2 }}>
          {isResultsLoading && <LinearProgress sx={{ mb: 2 }} />}
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2} alignItems="center" mb={2}>
            <TextField
              label="Search by stock code"
              size="small"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
            />
          </Stack>
          {!isResultsLoading && (!results || (results?.count || 0) === 0) ? (
            <Alert severity="info">No results yet — upload a CSV to see aggregates.</Alert>
          ) : (
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Stock Code</TableCell>
                  <TableCell align="right">Number Of Quotes Found</TableCell>
                  <TableCell align="right">Total Price</TableCell>
                  <TableCell>Created At</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {results?.results?.map((row: CsvResult) => (
                  <TableRow key={`${row.stock_code}-${row.created_at}`}>
                    <TableCell>{row.stock_code}</TableCell>
                    <TableCell align="right">{row.number_quotes_found}</TableCell>
                    <TableCell align="right">{Number(row.total_price).toLocaleString()}</TableCell>
                    <TableCell>{new Date(row.created_at).toLocaleString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
          <Stack alignItems="flex-end" mt={2}>
            <Pagination page={page} onChange={(_, p) => setPage(p)} count={Math.max(1, Math.ceil((results?.count || 0) / 25))} />
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
}
