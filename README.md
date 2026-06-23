<p align="center">
  <a href="https://github.com/Tibiritabara/cinescripter"><img src="./docs/logo/png/logo-no-background.png" alt="CineScripter"></a>
</p>
<p align="center">
    <em>CineScripter, supports your community, by enabling you to automatically create video content based own data</em>
</p>

---

**Source Code**: <a href="https://github.com/Tibiritabara/cinescripter" target="_blank">https://github.com/Tibiritabara/cinescripter</a>

---

CineScripter is a modern application, to generate video content based on your own data, harnessing the power of third parties for voice generation, multimedia generation, and text generation

The key features are:
* **Engaging**: Gathers fun images and gifs images, relevant to the script, to keep the audience engaged
* **Customizable**: Generate voice from this Text-To-Speech third party to successfully narrate your content
* **Context-based**: Generate a video script based on your own content and data
* **Extensible**: Quickly add new generation capabilities to add your own flavor to the content

## Requirements

Python 3.7+

CineScripter harnesses bespoke solutions for content generation:

* <a href="https://platform.openai.com/">OpenAI for the script generation</a>
* <a href="https://www.unsplash.com/">Unsplash for relevant media</a>
* <a href="https://developers.giphy.com/">Giphy for engaging media</a>
* <a href="https://beta.elevenlabs.io/">ElevenLabs for TTS</a>
* <a href="https://docs.60db.ai/">60db for TTS</a>
* <a href="https://weaviate.io" >Weaviate for Vector storage needs</a>

Please ensure having **API keys** for Giphy, OpenAI, Weaviate, and a TTS provider (ElevenLabs and/or 60db). For more details on which API keys are needed, please check the `./config/.env.dist` file.

## Text-To-Speech providers

CineScripter narrates each sentence of the generated script using a pluggable
Text-To-Speech (TTS) provider. Two providers are supported out of the box:

| Provider | Value for `TTS_PROVIDER` | API key | Voice id |
|----------|--------------------------|---------|----------|
| ElevenLabs | `elevenlabs` (default) | `ELEVEN_API_KEY` | `VOICE_ID` |
| 60db | `60db` (alias `sixtydb`) | `SIXTYDB_API_KEY` | `SIXTYDB_VOICE_ID` |

The active provider is selected at runtime via the `TTS_PROVIDER` environment
variable. No code changes are required to switch — just update your `.env`:

```bash
# Use ElevenLabs (default behaviour)
TTS_PROVIDER=elevenlabs
ELEVEN_API_KEY=your_elevenlabs_key
VOICE_ID=your_elevenlabs_voice_id

# Use 60db
TTS_PROVIDER=60db
SIXTYDB_API_KEY=sk_live_your_60db_key
SIXTYDB_VOICE_ID=your_60db_voice_id
```

60db uses the REST batch endpoint (`POST https://api.60db.ai/tts-synthesize`)
and authenticates with a `Bearer` token. You can tune the synthesis
(`output_format`, `speed`, `stability`, `similarity`, `enhance`) in the
`SIXTYDB` settings block in `src/utils/settings.py`. To discover the available
`voice_id` values for your account, call `GET https://api.60db.ai/myvoices`
(also exposed via `SixtyDB().list_voices()`).


