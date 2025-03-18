name: Update Maven artifacts for version {{ .updatecli_matrix_version }}

sources:
{{- range $key, $artifact := .artifacts }}
  {{- if all $artifact.updatecli_matrix_component_key $artifact.artifact_name_file $artifact.artifact_name_key $artifact.artifact_version_key }}
  src_{{ $key }}_artifact_name:
    name: {{ $key }} artifact name
    kind: yaml
    spec:
      file: {{ $artifact.artifact_name_file }}
      key: {{ $artifact.artifact_name_key }}
  src_{{ $key }}:
    name: {{ $key }} artifact
    kind: maven
    spec:
      repository: {{ requiredEnv "NEXUS_USERNAME" }}:{{ requiredEnv "NEXUS_PASSWORD" }}@nexus.alfresco.com/nexus/repository/{{ $artifact.artifact_repository_name | default $.ansible_default_repository_name }}
      groupid: {{ $artifact.artifact_group_id | default $.ansible_default_group_id }}
      artifactid: '{{ source (printf "src_%s_artifact_name" $key) }}'
      dependson:
      - src_{{ $key }}_artifact_name
      {{- $matrix_filter := index $ "matrix" $.updatecli_matrix_version $artifact.updatecli_matrix_component_key }}
      {{- if $matrix_filter }}
      {{- $pattern := index $matrix_filter "pattern" }}
      {{- $version := index $matrix_filter "version" }}
      versionFilter:
        kind: {{ if $pattern }}regex{{ else }}semver{{ end }}
        pattern: >-
          {{- if $pattern }}
          ^{{ $version }}{{ $pattern }}$
          {{- else }}
          {{ $version }}
          {{- end }}
      {{- end }}
  {{- end }}
{{- end }}

targets:
{{- range $key, $artifact := .artifacts }}
  {{- if all $artifact.updatecli_matrix_component_key (or $artifact.ansible_version_file $.ansible_version_file) $artifact.artifact_version_key }}
  yml_{{ $key }}:
    name: {{ $key }} yml
    kind: yaml
    sourceid: src_{{ $key }}
    spec:
      file: "{{ $artifact.ansible_version_file | default $.ansible_version_file }}"
      key: "{{ $artifact.artifact_version_key }}"
  {{- end }}
{{- end }}
