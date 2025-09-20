"use client";
import { useEffect, useState } from "react";
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

export default function Home() {
  const queryClient = useQueryClient();
  const { taskId, setTaskId } = useUploadStore();
  const [file, setFile] = useState<File | null>(null);
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [page, setPage] = useState(1);
  const [isUploading, setIsUploading] = useState(false);
  const [completedNotified, setCompletedNotified] = useState(false);

  useEffect(() => {
    const id = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(id);
  }, [search]);

  const { data: results, isLoading: isResultsLoading } = useQuery({
    queryKey: ["results", { search: debouncedSearch, page }],
    queryFn: () => api.listResults({ search: debouncedSearch, page }),
  });

  const { data: status } = useQuery({
    queryKey: ["task", taskId],
    queryFn: () => api.taskStatus(taskId!),
    enabled: Boolean(taskId),
    refetchInterval: (q) => (q.state.data?.state === "SUCCESS" || q.state.data?.state === "FAILURE" ? false : 1500),
  });

  const toast = useToastStore();
  const onUpload = async () => {
    if (!file) return;
    try {
      setIsUploading(true);
      const res = await api.uploadCsv(file);
      setTaskId(res.task_id);
      toast.show("Upload started", "success");
    } catch (e: any) {
      toast.show(e.message || "Upload failed", "error");
    } finally {
      setIsUploading(false);
    }
  };

  useEffect(() => {
    if (status?.state === "SUCCESS" && !completedNotified) {
      setCompletedNotified(true);
      queryClient.invalidateQueries({ queryKey: ["results"] });
      toast.show("Processing complete", "success");
    }
  }, [status?.state, completedNotified, queryClient, toast]);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Stack spacing={3}>
        <Typography variant="h4">CSV Analyzer</Typography>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} alignItems="center">
          <Button variant="contained" component="label">
            Choose CSV
            <input hidden type="file" accept=".csv,text/csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          </Button>
          <Typography variant="body2">{file?.name || "No file selected"}</Typography>
          <Button variant="outlined" onClick={onUpload} disabled={!file || isUploading}>
            {isUploading ? "Uploading..." : "Upload"}
          </Button>
        </Stack>

        {taskId && (
          <Alert severity="info">
            Task {taskId} — {status?.state || "PENDING"}
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
              {results?.results?.map((row: any) => (
                <TableRow key={`${row.stock_code}-${row.created_at}`}>
                  <TableCell>{row.stock_code}</TableCell>
                  <TableCell align="right">{row.number_quotes_found}</TableCell>
                  <TableCell align="right">{row.total_price}</TableCell>
                  <TableCell>{new Date(row.created_at).toLocaleString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <Stack alignItems="flex-end" mt={2}>
            <Pagination page={page} onChange={(_, p) => setPage(p)} count={Math.max(1, Math.ceil((results?.count || 0) / 25))} />
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
}
