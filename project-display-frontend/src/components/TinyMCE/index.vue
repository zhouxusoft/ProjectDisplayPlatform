<template>
  <div>
    <div
      class="tinymce-container editor-container"
      :class="{ fullscreen: fullscreen }"
    >
      <textarea :id="tinymceId" class="tinymce-textarea"></textarea>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import axios from 'axios'

// 如果需要引入上传 HTML 片段的接口，请取消下一行的注释并根据项目路径调整
// import { uploadHtml } from '@/api/upload'

// 定义组件的 Props
const props = defineProps({
  html: {
    type: String,
    default: ''
  },
  toolbar: {
    type: Array,
    default: () => []
  },
  menubar: {
    type: Boolean,
    default: false
  }
})

// 定义组件的 Emits
const emit = defineEmits(['update:modelValue'])

const hasChange = ref(false)
const hasInit = ref(false)
const tinymceId = `vue-tinymce-${Date.now()}`
const fullscreen = ref(false)
const value = ref(props.html) // 双向绑定的值
const editorContent = ref('')

// 监听 `value` 的变化并更新编辑器内容
watch(value, (newVal) => {
  nextTick(() => {
    const editor = window.tinymce.get(tinymceId)
    if (editor) {
      editor.setContent(newVal || '')
    }
  })
})

// 初始化 TinyMCE 编辑器
const initTinymce = () => {
  window.tinymce.init({
    selector: `#${tinymceId}`,
    height: 650,
    min_height: 560,
    language: 'zh_CN',
    menubar: false,
    license_key: 'gpl',
    plugins:
        'wordcount visualchars visualblocks template save preview pagebreak nonbreaking media insertdatetime importcss image help fullscreen directionality codesample code charmap link code table lists anchor autolink autoresize',
    toolbar:
        "undo redo forecolor backcolor codesample image media outdent indent aligncenter alignleft alignright alignjustify lineheight quicklink hr blockquote numlist bullist table link removeformat | underline bold italic strikethrough h2 h3  preview",
    fontsize_formats: '12px 14px 16px 18px 20px 24px 36px',
    body_class: 'panel-body',
    object_resizing: true,
    end_container_on_empty_block: true,
    powerpaste_word_import: 'clean',
    code_dialog_height: 450,
    code_dialog_width: 1000,
    default_link_target: '_blank',
    link_title: false,
    statusbar: false,
    setup(editor) {
      // 监控全屏状态变化
      editor.on('FullscreenStateChanged', (e) => {
        fullscreen.value = e.state
      })

      // 监听内容变化
      editor.on('NodeChange Change KeyUp SetContent', () => {
        hasChange.value = true
        const content = editor.getContent()
        // console.log(content)
        editorContent.value = content
        emit('update:modelValue', content)
      })
    },
    init_instance_callback: (editor) => {
      if (props.html) {
        editor.setContent(props.html)
      }
      hasInit.value = true
    }
  })
}

// 销毁 TinyMCE 编辑器
const destroyTinymce = () => {
  const editor = window.tinymce.get(tinymceId)
  if (editor) {
    editor.destroy()
  }
}

// 设置编辑器内容
const setContent = (content) => {
  const editor = window.tinymce.get(tinymceId)
  if (editor) {
    editor.setContent(content)
  }
}

// 获取编辑器内容
const getContent = () => {
  const editor = window.tinymce.get(tinymceId)
  return editor ? editor.getContent() : ''
}

// 图片上传成功后填充到富文本编辑器
const imageSuccess = async (urlList) => {
  try {
    let imageTemplateList = ''
    urlList.forEach(item => {
      const image = `<img style="max-width:100%;" src="${item}">`
      imageTemplateList += image
    })
    const editor = window.tinymce.get(tinymceId)
    if (editor) {
      editor.insertContent(imageTemplateList)
    }
    // 假设使用的是 Element Plus 的消息提示组件
    if (window.$message) {
      window.$message({
        message: '上传成功！',
        type: 'success'
      })
    }
  } catch (error) {
    console.error(error)
    if (window.$message) {
      window.$message({
        message: error.message || '上传失败',
        type: 'error'
      })
    }
  }
}

// 编辑器内容上传到 COS，调用返回 URL（如果需要）
/*
const content2Url = async () => {
  try {
    const res = await uploadHtml(editorContent.value)
    return res
  } catch (error) {
    if (window.$message) {
      window.$message({
        message: error.data.message || '上传失败',
        type: 'error'
      })
    }
  }
}
*/

// 生命周期钩子
onMounted(() => {
  initTinymce()
})

onBeforeUnmount(() => {
  destroyTinymce()
})
</script>

<style scoped lang="scss">
#tinymce p {
  margin: 0;
}

.tinymce {
  padding: 20px;
  border-radius: 10px;
  background: #fff;
  width: 100%;
}

.tinymce-container {
  position: relative;
  width: 100%;
}

.tinymce-textarea {
  visibility: hidden;
  z-index: -1;
}

.editor-custom-btn-container {
  position: absolute;
  right: 4px;
  top: 4px;
  /* z-index: 2005; */
}

.fullscreen .editor-custom-btn-container {
  z-index: 10000;
  position: fixed;
}

.editor-upload-btn {
  display: inline-block;
}

// 隐藏底部 logo 栏
.mce-edit-area + .mce-statusbar {
  opacity: 0;
  height: 0;
}
</style>