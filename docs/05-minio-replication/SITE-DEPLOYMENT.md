# DEV-909: independent distributed sites

`compose/minio/site-replication/sitea.yaml` and `siteb.yaml` each create four isolated server processes, four dedicated volumes, and an independent Docker bridge network. Site A defaults to 127.0.0.1:9700, site B to 127.0.0.1:9800.

Use `scripts/lab/dev909-site-replication.sh plan` first. With explicit approval, `start` starts both stacks. Configure two version-compatible `mc` aliases; verify each site with `mc admin info`. Ensure site B is empty, both sites share compatible identity-provider configuration, and no conflicting bucket replication exists. Then `configure` invokes `mc admin replicate add`, `info`, and `status` with captured output.

**Important:** Localhost-only published ports cannot serve as cross-site peer addresses from inside containers. Before configuring replication, provide stable peer-reachable endpoints (e.g. the provisioned `site-peer-net` shared Docker network with verified site-facing endpoints) and confirm bidirectional connectivity. The site containers share `site-peer-net` for peer traffic; the published localhost endpoints are only for host-side CLI. Peer connectivity and endpoint suitability must be verified before `configure`. Site-replication automation is therefore not yet end-to-end executable.

On 16GB RAM, two four-node sites may fit under tuned resource limits but require measurement. Do EXECUTION REQUIRED them alongside expansion or other heavy stacks. These are logical fault domains on one physical host, not real disaster recovery.

Evidence: server versions/digests, topology, site admin info, site replication config/status, bucket/IAM sync, object SHA-256, negative tests, peer outage/recovery, actual timestamps.

**Live acceptance:** EXECUTION REQUIRED.
