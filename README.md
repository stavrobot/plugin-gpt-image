# gpt-image plugin

Generate images from text prompts using OpenAI's gpt-image-1 model.

## Install

Ask Stavrobot to install `https://github.com/stavrobot/plugin-gpt-image`.

## Configuration

Set `api_key` in `config.json` with your OpenAI API key:

```json
{
  "api_key": "sk-..."
}
```

Obtain an API key at https://platform.openai.com/api-keys.

## Tool parameters

### generate_image

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | yes | Text prompt describing the image to generate. |
| `size` | string | no | Image size. One of: `1024x1024`, `1536x1024`, `1024x1536`. Defaults to `1024x1024`. |
| `quality` | string | no | Image quality. One of: `low`, `medium`, `high`. Defaults to `medium`. |
| `output_format` | string | no | Output format. One of: `png`, `jpeg`, `webp`. Defaults to `png`. |
