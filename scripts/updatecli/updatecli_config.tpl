name: ACS update pipeline

scms:
  acsRepo:
    kind: git
    spec:
        url: https://github.com/Alfresco/acs-packaging.git
        branch: master
        directory: '/tmp/updatecli/acs'
  acsEntRepo:
    kind: git
    spec:
        url: git@github.com:Alfresco/alfresco-enterprise-repo.git
        branch: master
        directory: '/tmp/updatecli/acsEnt'
  accRepo:
    kind: git
    spec:
      url: git@github.com:Alfresco/alfresco-applications.git
      branch: develop
      directory: '/tmp/updatecli/acc'
  adwRepo:
    kind: git
    spec:
      url: https://github.com/Alfresco/alfresco-content-app.git
      branch: master
      directory: '/tmp/updatecli/adw'
  aosAmpRepo:
    kind: git
    spec:
      url: git@github.com:Alfresco/alfresco-aos-module.git
      branch: master
      directory: '/tmp/updatecli/aos-amp'
  googleDriveAmpRepo:
    kind: git
    spec:
      url: git@github.com:Alfresco/googledrive.git
      branch: master
      directory: '/tmp/updatecli/googledrive'
  apiExplorerRepo:
    kind: git
    spec:
        url: https://github.com/Alfresco/rest-api-explorer.git
        branch: master
        directory: '/tmp/updatecli/api-explorer'
  dsyncRepo:
    kind: git
    spec:
      url: git@github.com:Alfresco/dsync-services.git
      branch: master
      directory: '/tmp/updatecli/dsync'
  searchRepo:
    kind: git
    spec:
      url: git@github.com:Alfresco/InsightEngine.git
      branch: master
      directory: '/tmp/updatecli/search'
  searchEnterpriseRepo:
    kind: git
    spec:
      url: git@github.com:Alfresco/alfresco-elasticsearch-connector.git
      branch: master
      directory: '/tmp/updatecli/search_enterprise'
  transformRepo:
    kind: git
    spec:
      url: git@github.com:Alfresco/alfresco-transform-core.git
      branch: master
      directory: '/tmp/updatecli/transform'
  trouterRepo:
    kind: git
    spec:
      url: git@github.com:Alfresco/alfresco-transform-service.git
      branch: master
      directory: '/tmp/updatecli/trouter'

# Available selectors: https://github.com/Masterminds/semver#basic-comparisons
sources:
  acs:
    name: ACS {{ .acs.version }}.x
    kind: gittag
    scmid: acsRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .acs.version }}(.(\d+))+{{ .version_pattern }}'
  {{- if and .acc .acc.version }}
  acc:
    name: ACC {{ .acc.version }}
    kind: gittag
    scmid: accRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .acc.version }}(.(\d+))+{{ .version_pattern }}'
  {{- end }}
  {{- if and .adw .adw.version }}
  adw:
    name: ADW {{ .adw.version }}
    kind: gittag
    scmid: adwRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .adw.version }}(.(\d+))+{{ .version_pattern }}'
  {{- end }}
  {{- if and .ags .ags.version }}
  agsAmp:
    name: AGS AMP {{ .ags.version }}.x
    kind: gittag
    scmid: acsEntRepo
    spec:
      versionFilter:
        kind: regex
        pattern: 'ags-{{ .ags.version }}(.(\d+))+{{ .version_pattern }}'
    transformers:
      - trimprefix: "ags-"
  {{- end }}
  aosAmp:
    name: AOS AMP {{ .aos.version }}
    kind: gittag
    scmid: aosAmpRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .aos.version }}(.(\d+))+{{ .version_pattern }}'
  googleDriveAmp:
    name: Google Drive AMP {{ .googleDrive.version }}
    kind: gittag
    scmid: googleDriveAmpRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .googleDrive.version }}(.(\d+))+{{ .version_pattern }}'
  apiExplorer:
    name: Api explorer {{ .apiExplorer.version }}
    kind: gittag
    scmid: apiExplorerRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .apiExplorer.version }}(.(\d+))+{{ .version_pattern }}'
  {{- if and .dsync .dsync.version }}
  dsync:
    name: Desktop Sync {{ .dsync.version }}
    kind: gittag
    scmid: dsyncRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .dsync.version }}(.(\d+))+{{ .version_pattern }}'
  {{- end }}
  search:
    name: InsightEngine {{ .search.version }}
    kind: gittag
    scmid: searchRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .search.version }}(.(\d+))+{{ .version_pattern }}'
  {{- if and .searchEnterprise .searchEnterprise.version }}
  searchEnterprise:
    name: Search Enterprise {{ .searchEnterprise.version }}
    kind: gittag
    scmid: searchEnterpriseRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .searchEnterprise.version }}(.(\d+))+{{ .version_pattern }}'
  {{- end }}
  transform:
    name: Transform Core {{ .transform.version }}
    kind: gittag
    scmid: transformRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .transform.version }}(.(\d+))+{{ .version_pattern }}'
  {{- if and .trouter .trouter.version }}
  trouter:
    name: ATS Transform Service {{ .trouter.version }}
    kind: gittag
    scmid: trouterRepo
    spec:
      versionFilter:
        kind: regex
        pattern: '{{ .trouter.version }}(.(\d+))+{{ .version_pattern }}'
  {{- end }}

targets:
  {{- if index . "targets" "main" }}
  acs:
    name: Bump acs
    kind: yaml
    sourceid: acs
    spec:
      key: acs.version
      file: '{{ .target_file }}'
  {{- if and .acc .acc.version }}
  acc:
    name: Bump acc
    kind: yaml
    sourceid: acc
    spec:
      key: acc.version
      file: '{{ .target_file }}'
  {{- end }}
  {{- if and .adw.version }}
  adw:
    name: Bump adw
    kind: yaml
    sourceid: adw
    spec:
      key: adw.version
      file: '{{ .target_file }}'
  {{- end }}
  apiExplorer:
    name: Bump api-explorer
    kind: yaml
    sourceid: apiExplorer
    spec:
      key: api_explorer.version
      file: '{{ .target_file }}'
  {{- if and .dsync .dsync.version }}
  dsync:
    name: Bump sync
    kind: yaml
    sourceid: dsync
    spec:
      key: sync.version
      file: '{{ .target_file }}'
  {{- end }}
  search:
    name: Bump InsightEngine
    kind: yaml
    sourceid: search
    spec:
      key: search.version
      file: '{{ .target_file }}'
  {{- if and .searchEnterprise .searchEnterprise.version }}
  searchEnterprise:
    name: Bump Search Enterprise
    kind: yaml
    sourceid: searchEnterprise
    spec:
      key: search_enterprise.version
      file: '{{ .target_file }}'
  {{- end }}
  transform:
    name: Bump Transform Core
    kind: yaml
    sourceid: transform
    spec:
      key: transform.version
      file: '{{ .target_file }}'
  {{- if and .trouter .trouter.version }}
  trouter:
    name: Bump ATS Transform Service
    kind: yaml
    sourceid: trouter
    spec:
      key: trouter.version
      file: '{{ .target_file }}'
  {{- end }}
  {{- if and .sfs .sfs.version }}
  sfs:
    name: Bump Shared File Store
    kind: yaml
    sourceid: trouter
    spec:
      key: sfs.version
      file: '{{ .target_file }}'
  {{- end }}
  {{- end }}
  {{ range $index, $element := index . "targets" "amps" }}
  {{ $indexAmp := printf "%s%s" $index "Amp"}}
  {{- if index $ $index }}
  {{ $indexAmp }}:
    name: Bump {{ $index }} AMP
    kind: yaml
    sourceid: {{ $element.sourceid }}
    spec:
      key: amps.{{ $element.key_selector }}.version
      file: {{ $.target_file }}
  {{- end }}
  {{- end }}
