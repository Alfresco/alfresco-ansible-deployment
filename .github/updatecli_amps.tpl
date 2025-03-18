name: Update AMPs artifacts for version {{ .updatecli_matrix_version }} in {{ .ansible_version_file }}

scms:
  acsPackaging:
    kind: github
    spec:
      owner: Alfresco
      repository: acs-packaging
      branch: {{ .updatecli_amps_release_branch }}
      token: {{ requiredEnv "UPDATECLI_GITHUB_TOKEN" }}
      username: {{ requiredEnv "UPDATECLI_GITHUB_USERNAME" }}
  acsEntRepo:
    kind: github
    spec:
      owner: Alfresco
      repository: alfresco-enterprise-repo
      branch: {{ .updatecli_amps_release_branch }}
      token: {{ requiredEnv "UPDATECLI_GITHUB_TOKEN" }}
      username: {{ requiredEnv "UPDATECLI_GITHUB_USERNAME" }}
  acsComRepo:
    kind: github
    spec:
      owner: Alfresco
      repository: alfresco-community-repo
      branch: {{ .updatecli_amps_release_branch }}
      token: {{ requiredEnv "UPDATECLI_GITHUB_TOKEN" }}
      username: {{ requiredEnv "UPDATECLI_GITHUB_USERNAME" }}

sources:
{{- range $key, $artifact := .artifacts }}
  {{- if all $artifact.updatecli_xml_target $artifact.updatecli_scm_id }}
  src_{{ $key }}:
    name: {{ $key }} artifact
    scmid: {{ $artifact.updatecli_scm_id }}
    kind: xml
    spec:
      file: pom.xml
      path: "{{ $artifact.updatecli_xml_target }}"
  {{- end }}
{{- end }}

targets:
{{- range $key, $artifact := .artifacts }}
  {{- if all $artifact.updatecli_xml_target $artifact.updatecli_scm_id $artifact.artifact_version_key }}
  yml_{{ $key }}:
    name: {{ $key }} yml
    kind: yaml
    sourceid: src_{{ $key }}
    spec:
      file: "{{ $.ansible_version_file }}"
      key: "{{ $artifact.artifact_version_key }}"
  {{- end }}
{{- end }}
