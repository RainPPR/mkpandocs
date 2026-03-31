-- link_class.lua
-- 为外部链接添加 CSS class="external"
function Link(el)
  if el.target:match("^https?://") then
    el.attributes.class = (el.attributes.class or "") .. " external"
    el.target = el.target
  end
  return el
end
