import cors from "cors";
import express from "express";
import morgan from "morgan";
import { attachVendorCode, requireAuth } from "./src/auth.js";
import routes from "./src/routes.js";

const app = express();
const port = process.env.PORT || 8085;

app.use(cors());
app.use(express.json());
app.use(morgan("tiny"));

// Public health endpoint for platform checks.
app.get("/healthz", (_req, res) => {
  return res.json({ status: "ok", service: "integration-hub-mock-payers" });
});

// Protected API endpoints require a valid JWT and vendor claim.
app.use(requireAuth, attachVendorCode, routes);

app.listen(port, () => {
  console.log(`[mock-payers] listening on port ${port}`);
});
