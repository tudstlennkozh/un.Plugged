
function skin_name()
    if name == nil then
        name = SKIN:GetVariable('CURRENTCONFIG')
    end
    return name
end

function log(szString)
    print(skin_name() .. " (Actions.lua):" .. szString)
end

function Initialize()
    log("in Initialize")
end

function split(s, delimiter)
    local result = {};
    for match in (s..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match);
    end
    return result;
end

function remove_chars(s, remove)
    return (s:gsub("["..remove.."]+", ""))
end

function _change_skin_state(state)
    log('in _change_skin_state(' .. tostring(state) .. ')')
    local bang_cmd
    local OtherSkins
    if state then
        bang_cmd = "!ActivateConfig"
    else
        bang_cmd = "!DeactivateConfig"
    end
    OtherSkins =  SKIN:GetVariable('OtherSkins')
    log(bang_cmd)
    log(OtherSkins)
   if OtherSkins ~= nil then
        local allskins = split(OtherSkins, "|")
        local skin_name, ini_name, skin_param
        for k, v in pairs(allskins) do
            local details = split(v, "\+")
            for num,value in pairs(details) do
                if num == 1 then
                    skin_name = remove_chars(value, "\"")
                else
                    ini_name = remove_chars(value, "\"")
                    if state then
                        skin_param = ini_name
                    else
                        skin_param = ""
                    end
                end
            end
            SKIN:Bang(bang_cmd, skin_name, skin_param)
            log("cmd:" .. bang_cmd .. "; skin_name:" .. skin_name .. "; param:" .. skin_param)
        end
   end
end

function activate_skins()
    _change_skin_state(true)
    return True
end

function deactivate_skins()
    _change_skin_state(false)
    return False
end

-- tests
OtherSkins = 'Win10 Widgets\\Weather"+"Weather-ExtraLarge.ini"|"Win10 Widgets\\Performance - CPU"+"CPU-Small.ini"|"Win10 Widgets\\Performance - Network"+"Network-Small.ini'
print(OtherSkins)
list=split(OtherSkins, '|')
for k,v in pairs(list) do
    print("block "..k)
    local details = split(v, '\+')
    local name
    local ini_name
    for num,value in pairs(details) do
        if num == 1 then
            name = remove_chars(value, "\"")
        else
            ini_name = remove_chars(value, "\"")
        end
    end
    print("name:" .. name .. "\nini:" .. ini_name)
end


