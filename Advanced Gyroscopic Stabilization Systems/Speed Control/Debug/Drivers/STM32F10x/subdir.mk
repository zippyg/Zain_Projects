################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/STM32F10x/system_stm32f10x.c 

OBJS += \
./Drivers/STM32F10x/system_stm32f10x.o 

C_DEPS += \
./Drivers/STM32F10x/system_stm32f10x.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/STM32F10x/%.o Drivers/STM32F10x/%.su Drivers/STM32F10x/%.cyclo: ../Drivers/STM32F10x/%.c Drivers/STM32F10x/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F767xx -c -I"C:/Users/13410/Desktop/study/Summer Project Year 1/Speed Control/Drivers/MPU6050-master/Src" -I"C:/Users/13410/Desktop/study/Summer Project Year 1/Speed Control/Drivers/STM32F10x" -I"C:/Users/13410/Desktop/study/Summer Project Year 1/Speed Control/Drivers/STM32F7xx_Nucleo_144" -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Drivers-2f-STM32F10x

clean-Drivers-2f-STM32F10x:
	-$(RM) ./Drivers/STM32F10x/system_stm32f10x.cyclo ./Drivers/STM32F10x/system_stm32f10x.d ./Drivers/STM32F10x/system_stm32f10x.o ./Drivers/STM32F10x/system_stm32f10x.su

.PHONY: clean-Drivers-2f-STM32F10x

