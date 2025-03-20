name: Update AMI

sources:
{{- range $key, $ami := .amis }}
  src_{{ $key }}:
    kind: aws/ami
    spec:
      region: {{ requiredEnv "AWS_REGION" }}
      filters:
        - name: "owner-id"
          values: "{{ $ami.owner_id | default "*" }}"
        - name: "name"
          values: "{{ $ami.pattern }}"
        - name: "architecture"
          values: "{{ $ami.architecture | default "x86_64" }}"
        - name: "block-device-mapping.volume-type"
          values: "{{ $ami.volume_type | default "gp3" }}"
{{- end }}

targets:
{{- range $key, $target := .targets }}
  yml_{{ $key }}:
    kind: yaml
    sourceid: src_{{ $target.source }}
    spec:
      file: "{{ $target.file }}"
      key: "{{ $target.key }}"
{{- end }}
