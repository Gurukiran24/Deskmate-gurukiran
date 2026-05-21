Release / Model hosting instructions
=================================

This document explains recommended ways to host the large `model/` artifact outside of normal Git commits, and how to add a download link to this repository.

Options
-------

1) GitHub Release (recommended for simple workflows)

   - Create a release on GitHub (via web UI or `gh` CLI) and upload the model binary as a release asset.
   - Example using `gh` (GitHub CLI):

     ```powershell
     gh release create v1.0.0 path/to/model/pytorch_model.bin --title "Model v1.0.0" --notes "Trained model artifact"
     ```

   - After uploading, copy the release asset URL and update `README.md` under "Model download".

2) AWS S3 (recommended for larger teams / automation)

   - Upload with `awscli`:

     ```powershell
     aws s3 cp path/to/model/pytorch_model.bin s3://your-bucket/path/pytorch_model.bin --acl private
     aws s3 presign s3://your-bucket/path/pytorch_model.bin --expires-in 604800
     ```

   - Use a presigned URL or IAM-secured access and add the download link to `README.md`.

3) Google Drive / Shared Drive

   - Upload the file in the browser and create a shareable link.
   - Alternatively use a CLI tool to upload programmatically.

Notes about Git LFS migration
----------------------------

- If you prefer the model inside the repository but stored by LFS, initialize LFS locally then migrate:

  ```powershell
  git lfs install
  git lfs track "model/*.bin"
  git add .gitattributes
  git commit -m "Track model binaries with Git LFS"
  git lfs migrate import --include="model/*.bin" --everything
  git push origin --force --all
  ```

- Migration rewrites history; collaborators must re-clone after forced push.

Checklist for adding a hosted model link
--------------------------------------

- [ ] Upload model to chosen provider
- [ ] Copy public or presigned download URL
- [ ] Replace placeholder link in `README.md` (Model download section)
- [ ] Commit and push the `README.md` update

If you want, I can prepare the upload (instructions) or add the final download link once you provide the URL or grant me access details for your storage.
