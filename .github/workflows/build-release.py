# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python
name: Python application
on:
  push:
    # Sequence of patterns matched against refs/tags
    tags:
    - 'v*' # Push events to matching v*, i.e. v1.0, v20.15.10
jobs:
  setuprelease:
    name: Build linux and setup release
    runs-on: ubuntu-latest
    outputs:
      upload_url: ${{ steps.create_release.outputs.upload_url }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python 3.10
        uses: actions/setup-python@v3
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install setuptools
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Build project # This would actually build your project, using zip for an example artifact
        run: |
          pyinstaller --windowed --onefile main.py -y; cp ./bookstats/badwords ./dist/badwords; cp ./bookstats/exclude_from_wordlist ./dist/exclude_from_wordlist; mv ./dist/main ./dist/bookstats; tar -czf bookstats-ubuntu.tar.gz -C ./dist $(ls ./dist);
      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
      - name: Upload Release Asset
        id: upload-release-asset 
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }} # This pulls from the CREATE RELEASE step above, referencing it's ID to get its outputs object, which include a `upload_url`. See this blog post for more info: https://jasonet.co/posts/new-features-of-github-actions/#passing-data-to-future-steps 
          asset_path: bookstats.tar.gz
          asset_name: bookstats.tar.gz
          asset_content_type: application/tar+gzip
  windowsbuild:
    name: Build for windows and upload zip
    runs-on: setuprelease
    needs: job1
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install setuptools
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Build project # This would actually build your project, using zip for an example artifact
        run: |
          pyinstaller --windowed --onefile main.py -y; Copy-Item bookstats\badwords -Destination dist\badwords;
          Copy-Item bookstats\exclude_from_wordlist -Destination dist\exclude_from_wordlist;
          Rename-Item -Path dist\main.exe dist\bookstats.exe; Compress-Archive -Path dist\* -CompressionLabel Optimal -DestinationPath bookstats-win.zip;
    - name: Upload Release Asset
        id: upload-release-asset 
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ needs.setuprelease.outputs.upload_url }} # This pulls from the CREATE RELEASE step above, referencing it's ID to get its outputs object, which include a `upload_url`. See this blog post for more info: https://jasonet.co/posts/new-features-of-github-actions/#passing-data-to-future-steps 
          asset_path: bookstats-win.zip
          asset_name: bookstats-win.zip
          asset_content_type: application/tar+gzip



name: Upload Release Asset